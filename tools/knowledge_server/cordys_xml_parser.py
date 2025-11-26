"""
Cordys/OpenText BPM XML Parser
Extracts detailed information from Cordys metadata files for comprehensive documentation
"""

import xml.etree.ElementTree as ET
from typing import Dict, List, Any, Optional
from loguru import logger

class CordysXMLParser:
    """Parse Cordys/OpenText BPM XML metadata files"""
    
    def parse_script(self, xml_content: str, file_path: str) -> Dict[str, Any]:
        """
        Parse a script file (script_*.xml)
        Extracts: name, parameters, logic snippet
        """
        try:
            root = ET.fromstring(xml_content)
            
            script_data = {
                "type": "script",
                "name": root.get('name', ''),
                "label": self._get_text(root, 'label'),
                "description": self._get_text(root, 'description'),
                "file_path": file_path,
                "parameters": [],
                "logic_snippet": ""
            }
            
            # Extract parameters
            param_list = root.find('parameterList')
            if param_list is not None:
                for param in param_list.findall('parameter'):
                    param_data = {
                        "name": param.get('name', ''),
                        "type": param.get('type', ''),
                        "data_type": self._get_text(param, 'type')
                    }
                    script_data['parameters'].append(param_data)
            
            # Extract FULL BUSINESS LOGIC (for comprehensive documentation)
            script_elem = root.find('script')
            if script_elem is not None and script_elem.text:
                logic = script_elem.text.strip()
                # Store first 5000 chars for detailed analysis (increased from 500)
                script_data['logic_snippet'] = logic[:5000] + ('...' if len(logic) > 5000 else '')
                script_data['logic_length'] = len(logic)
            
            return script_data
            
        except Exception as e:
            logger.warning(f"Failed to parse script {file_path}: {e}")
            return {"type": "script", "file_path": file_path, "error": str(e)}
    
    def parse_interface(self, xml_content: str, file_path: str) -> Dict[str, Any]:
        """
        Parse an interface file (iface_*.xml)
        Extracts: service name, operations, input/output structures
        """
        try:
            root = ET.fromstring(xml_content)
            
            interface_data = {
                "type": "interface",
                "name": root.get('name', ''),
                "label": self._get_text(root, 'label'),
                "description": self._get_text(root, 'description'),
                "file_path": file_path,
                "operations": []
            }
            
            # Extract operations
            op_list = root.find('operationList')
            if op_list is not None:
                for op in op_list.findall('operation'):
                    op_data = {
                        "name": op.get('name', ''),
                        "type": self._get_text(op, 'type'),
                        "description": self._get_text(op, 'description'),
                        "input": self._get_text(op, 'input'),
                        "output": self._get_text(op, 'output')
                    }
                    interface_data['operations'].append(op_data)
            
            return interface_data
            
        except Exception as e:
            logger.warning(f"Failed to parse interface {file_path}: {e}")
            return {"type": "interface", "file_path": file_path, "error": str(e)}
    
    def parse_process(self, xml_content: str, file_path: str) -> Dict[str, Any]:
        """
        Parse a process file (proc_*.xml)
        Extracts: workflow name, activities, flow structure
        """
        try:
            root = ET.fromstring(xml_content)
            
            process_data = {
                "type": "process",
                "name": root.get('name', ''),
                "label": self._get_text(root, 'label'),
                "description": self._get_text(root, 'description'),
                "file_path": file_path,
                "activities": []
            }
            
            # Extract activities recursively
            self._extract_activities(root, process_data['activities'])
            
            return process_data
            
        except Exception as e:
            logger.warning(f"Failed to parse process {file_path}: {e}")
            return {"type": "process", "file_path": file_path, "error": str(e)}
    
    def parse_document(self, xml_content: str, file_path: str) -> Dict[str, Any]:
        """
        Parse a document file (doc_*.xml)
        Extracts: entity name, database schema, fields/columns
        """
        try:
            root = ET.fromstring(xml_content)
            
            doc_data = {
                "type": "document",
                "name": root.get('name', ''),
                "label": self._get_text(root, 'label'),
                "description": self._get_text(root, 'description'),
                "db_schema": self._get_text(root, 'dbSchema'),
                "extends": self._get_text(root, 'extends'),
                "file_path": file_path,
                "fields": []
            }
            
            # Extract variables (fields)
            var_list = root.find('variableList')
            if var_list is not None:
                for var in var_list.findall('variable'):
                    field_data = {
                        "name": var.get('name', ''),
                        "type": var.get('type', ''),
                        "column": self._get_text(var, 'column'),
                        "table": self._get_text(var, 'table'),
                        "value_type": self._get_text(var, 'valueType'),
                        "is_key": self._get_text(var, 'key') == '1'
                    }
                    doc_data['fields'].append(field_data)
            
            return doc_data
            
        except Exception as e:
            logger.warning(f"Failed to parse document {file_path}: {e}")
            return {"type": "document", "file_path": file_path, "error": str(e)}
    
    def parse_datatype(self, xml_content: str, file_path: str) -> Dict[str, Any]:
        """
        Parse a data type file (dtype_*.xml)
        Extracts: type definition, enumeration values
        """
        try:
            root = ET.fromstring(xml_content)
            
            dtype_data = {
                "type": "datatype",
                "name": root.get('name', ''),
                "label": self._get_text(root, 'label'),
                "description": self._get_text(root, 'description'),
                "file_path": file_path,
                "enum_values": []
            }
            
            # Extract enumeration values
            enum = root.find('.//enumeration')
            if enum is not None:
                value_list = enum.find('valueList')
                if value_list is not None:
                    for val in value_list.findall('value'):
                        dtype_data['enum_values'].append({
                            "name": val.get('name', ''),
                            "code": val.get('code', '')
                        })
            
            return dtype_data
            
        except Exception as e:
            logger.warning(f"Failed to parse datatype {file_path}: {e}")
            return {"type": "datatype", "file_path": file_path, "error": str(e)}
    
    def parse_service(self, xml_content: str, file_path: str) -> Dict[str, Any]:
        """
        Parse an external service file (service_*.xml)
        Extracts: service endpoints, ports, bindings
        """
        try:
            root = ET.fromstring(xml_content)
            
            service_data = {
                "type": "service",
                "name": root.get('name', ''),
                "label": self._get_text(root, 'label'),
                "description": self._get_text(root, 'description'),
                "file_path": file_path,
                "ports": []
            }
            
            # Extract ports
            port_list = root.find('portList')
            if port_list is not None:
                for port in port_list.findall('port'):
                    port_data = {
                        "name": port.get('name', ''),
                        "binding": self._get_text(port, 'binding'),
                        "description": self._get_text(port, 'description')
                    }
                    service_data['ports'].append(port_data)
            
            return service_data
            
        except Exception as e:
            logger.warning(f"Failed to parse service {file_path}: {e}")
            return {"type": "service", "file_path": file_path, "error": str(e)}
    
    def parse_binding(self, xml_content: str, file_path: str) -> Dict[str, Any]:
        """
        Parse a binding file (bind_*.xml)
        Extracts: SOAP binding details, operations, interface reference
        """
        try:
            root = ET.fromstring(xml_content)
            
            binding_data = {
                "type": "binding",
                "name": root.get('name', ''),
                "label": self._get_text(root, 'label'),
                "description": self._get_text(root, 'description'),
                "interface": self._get_text(root, 'interface'),
                "file_path": file_path,
                "extensions": []
            }
            
            # Extract extensions (SOAP actions, etc.)
            ext_list = root.find('extensionList')
            if ext_list is not None:
                for ext in ext_list.findall('extension'):
                    ext_data = {
                        "name": ext.get('name', ''),
                        "element": self._get_text(ext, 'element')
                    }
                    
                    # Extract element items
                    item_map = ext.find('elementItemMap')
                    if item_map is not None:
                        ext_data['items'] = {}
                        for item in item_map.findall('elementItem'):
                            key = item.get('key', '')
                            value = item.text if item.text else ''
                            ext_data['items'][key] = value
                    
                    binding_data['extensions'].append(ext_data)
            
            return binding_data
            
        except Exception as e:
            logger.warning(f"Failed to parse binding {file_path}: {e}")
            return {"type": "binding", "file_path": file_path, "error": str(e)}
    
    def parse_namespace(self, xml_content: str, file_path: str) -> Dict[str, Any]:
        """
        Parse a namespace file (nspace_*.xml)
        Extracts: module name and metadata
        """
        try:
            root = ET.fromstring(xml_content)
            
            return {
                "type": "namespace",
                "name": root.get('name', ''),
                "label": self._get_text(root, 'label'),
                "meta_version": self._get_text(root, 'metaVersion'),
                "file_path": file_path
            }
            
        except Exception as e:
            logger.warning(f"Failed to parse namespace {file_path}: {e}")
            return {"type": "namespace", "file_path": file_path, "error": str(e)}
    
    def parse_file(self, xml_content: str, file_path: str) -> Optional[Dict[str, Any]]:
        """
        Auto-detect file type and parse accordingly
        """
        file_name = file_path.split('/')[-1]
        
        try:
            if file_name.startswith('script_'):
                return self.parse_script(xml_content, file_path)
            elif file_name.startswith('iface_'):
                return self.parse_interface(xml_content, file_path)
            elif file_name.startswith('proc_'):
                return self.parse_process(xml_content, file_path)
            elif file_name.startswith('doc_'):
                return self.parse_document(xml_content, file_path)
            elif file_name.startswith('dtype_') or file_name.startswith('dstruct_'):
                return self.parse_datatype(xml_content, file_path)
            elif file_name.startswith('service_'):
                return self.parse_service(xml_content, file_path)
            elif file_name.startswith('bind_'):
                return self.parse_binding(xml_content, file_path)
            elif file_name.startswith('nspace_'):
                return self.parse_namespace(xml_content, file_path)
            else:
                return None  # Skip unknown types
                
        except Exception as e:
            logger.warning(f"Failed to parse {file_path}: {e}")
            return None
    
    # Helper methods
    
    def _get_text(self, element: ET.Element, tag: str) -> str:
        """Safely get text from an XML element"""
        child = element.find(tag)
        return child.text.strip() if child is not None and child.text else ""
    
    def _extract_activities(self, element: ET.Element, activities: List[Dict], depth: int = 0):
        """Recursively extract COMPREHENSIVE activity details from process"""
        if depth > 10:  # Increased depth for complex processes
            return
        
        for child in element:
            if child.tag in ['activity', 'child']:
                activity = {
                    "name": child.get('name', ''),
                    "type": child.get('type', ''),
                    "label": self._get_text(child, 'label'),
                    "description": self._get_text(child, 'description'),
                    "element": self._get_text(child, 'element')
                }
                
                # Extract CONDITIONS (decision logic)
                condition = child.find('condition')
                if condition is not None and condition.text:
                    activity['condition'] = condition.text.strip()[:1000]  # First 1000 chars
                
                # Extract MAPPINGS (data transformations)
                mappings = []
                mapping_list = child.find('mappingList')
                if mapping_list is not None:
                    for mapping in mapping_list.findall('mapping'):
                        mappings.append({
                            "from": self._get_text(mapping, 'from'),
                            "to": self._get_text(mapping, 'to'),
                            "expression": self._get_text(mapping, 'expression')
                        })
                if mappings:
                    activity['mappings'] = mappings
                
                # Extract SCRIPTS (inline business logic)
                script = child.find('script')
                if script is not None and script.text:
                    activity['inline_script'] = script.text.strip()[:1000]  # First 1000 chars
                
                # Extract ERROR HANDLING
                error_handler = child.find('errorHandler')
                if error_handler is not None:
                    activity['error_handler'] = {
                        "type": error_handler.get('type', ''),
                        "action": self._get_text(error_handler, 'action')
                    }
                
                # Extract PROPERTIES (configuration)
                properties = {}
                prop_list = child.find('propertyList')
                if prop_list is not None:
                    for prop in prop_list.findall('property'):
                        prop_name = prop.get('name', '')
                        prop_value = prop.text or prop.get('value', '')
                        properties[prop_name] = prop_value
                if properties:
                    activity['properties'] = properties
                
                # Check for sub-activities
                child_list = child.find('childList')
                if child_list is not None:
                    activity['children'] = []
                    self._extract_activities(child_list, activity['children'], depth + 1)
                
                activities.append(activity)


# Global instance
cordys_parser = CordysXMLParser()

