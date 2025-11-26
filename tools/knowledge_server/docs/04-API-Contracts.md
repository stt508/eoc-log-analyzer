---
**Auto-Generated Documentation**  
Generated: 2025-11-25T15:41:11.325404  
Branch: master  
Path: Trunk/FrontierOM  
**⚠️ Do not edit directly - regenerate from code**
---


# API Contracts

Expected inputs, outputs, and status codes for system APIs.

---


## Manageorderinterface.Manageorder.Submitorder

**Service:** DPI Submit Order Interface
**Operation:** SubmitOrder
**Type:** Request-Response
**Request_Structure:** dstruct_ManageOrder.ManageOrderSubmitOrderRequest
**Response_Structure:** dstruct_ManageOrder.ManageOrderSubmitOrderResponse
**Description:** Operation for the DPI SubmitOrder - billing update interface. This must be named SubmitOrder.
**File_Path:** Trunk/FrontierOM/metadata/ManageOrderInterface/iface_ManageOrder.xml

---

## Of.Tmpintf.Tmpintfrr

**Service:** tmpIntf
**Operation:** tmpIntfRR
**Type:** Request-Response
**Request_Structure:** 
**Response_Structure:** 
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/OF/iface_tmpIntf.xml

---

## Of.Triaddeffered.Triaddeferredintf

**Service:** triad deferred
**Operation:** triadDeferredIntf
**Type:** Notification
**Request_Structure:** dstruct_SubmitServiceOrder.invokeResponse
**Response_Structure:** 
**Description:** Operation for the deferred Triad activation resopnse that will be sent back into the flow via the listener.
**File_Path:** Trunk/FrontierOM/metadata/OF/iface_triadDeffered.xml

---

## Of.Wfmresolution.Dpiresolutionintf Ia

**Service:** WFM Resolution
**Operation:** dpiResolutionIntf_IA
**Type:** Notification
**Request_Structure:** dstruct_WFM.OrderCareResolution
**Response_Structure:** 
**Description:** Operation for wfmResolution - DPI_IA
**File_Path:** Trunk/FrontierOM/metadata/OF/iface_wfmResolution.xml

---

## Of.Wfmresolution.Dpiresolutionintf Disp

**Service:** WFM Resolution
**Operation:** dpiResolutionIntf_Disp
**Type:** Notification
**Request_Structure:** dstruct_WFM.OrderCareResolution
**Response_Structure:** 
**Description:** Operation for wfmResolution - DPI_Disp
**File_Path:** Trunk/FrontierOM/metadata/OF/iface_wfmResolution.xml

---

## Of.Wfmresolution.Tcresolutionintf Ia

**Service:** WFM Resolution
**Operation:** tcResolutionIntf_IA
**Type:** Notification
**Request_Structure:** dstruct_WFM.OrderCareResolution
**Response_Structure:** 
**Description:** Operation for wfmResolution - TC_IA
**File_Path:** Trunk/FrontierOM/metadata/OF/iface_wfmResolution.xml

---

## Of.Wfmresolution.Tcrespolutionintf Disp

**Service:** WFM Resolution
**Operation:** tcRespolutionIntf_Disp
**Type:** Notification
**Request_Structure:** dstruct_WFM.OrderCareResolution
**Response_Structure:** 
**Description:** Operation for wfmResolution - TC_Disp.
**File_Path:** Trunk/FrontierOM/metadata/OF/iface_wfmResolution.xml

---

## Of.Wfmresolution.Triadresolutionintf Ia

**Service:** WFM Resolution
**Operation:** triadResolutionIntf_IA
**Type:** Notification
**Request_Structure:** dstruct_WFM.OrderCareResolution
**Response_Structure:** 
**Description:** Operation for wfmResolution - Triad_IA
**File_Path:** Trunk/FrontierOM/metadata/OF/iface_wfmResolution.xml

---

## Of.Wfmresolution.Triadresolutionintf Disp

**Service:** WFM Resolution
**Operation:** triadResolutionIntf_Disp
**Type:** Notification
**Request_Structure:** dstruct_WFM.OrderCareResolution
**Response_Structure:** 
**Description:** Operationg for wfmResolution - Triad_Disp
**File_Path:** Trunk/FrontierOM/metadata/OF/iface_wfmResolution.xml

---

## Of.Wfmresolution.Customernotificationresolutionintf Ia

**Service:** WFM Resolution
**Operation:** customerNotificationResolutionIntf_IA
**Type:** Notification
**Request_Structure:** dstruct_WFM.OrderCareResolution
**Response_Structure:** 
**Description:** Operation for WFMResolution - CustomerNotification_IA
**File_Path:** Trunk/FrontierOM/metadata/OF/iface_wfmResolution.xml

---

## Of.Wfmresolution.Customernotificationresolutionintf Disp

**Service:** WFM Resolution
**Operation:** customerNotificationResolutionIntf_Disp
**Type:** Notification
**Request_Structure:** dstruct_WFM.OrderCareResolution
**Response_Structure:** 
**Description:** WFM resolution for CustomerNotification_Disp
**File_Path:** Trunk/FrontierOM/metadata/OF/iface_wfmResolution.xml

---

## Of.Wfmresolution.Cantriadintf Ia

**Service:** WFM Resolution
**Operation:** canTriadIntf_IA
**Type:** Notification
**Request_Structure:** dstruct_WFM.OrderCareResolution
**Response_Structure:** 
**Description:** Participant for Triad during the cancellation flow.
**File_Path:** Trunk/FrontierOM/metadata/OF/iface_wfmResolution.xml

---

## Of.Wfmresolution.Dpiumresolutionintf Ia

**Service:** WFM Resolution
**Operation:** dpiUMResolutionIntf_IA
**Type:** Notification
**Request_Structure:** dstruct_WFM.OrderCareResolution
**Response_Structure:** 
**Description:** Operation for wfmResolution - DPI UpdateMemo
**File_Path:** Trunk/FrontierOM/metadata/OF/iface_wfmResolution.xml

---

## Schedulemanagement.Schedulemanagement.Cancelappointment

**Service:** ScheduleManagement
**Operation:** CancelAppointment
**Type:** Request-Response
**Request_Structure:** dstruct_ScheduleManagement.CancelAppointment
**Response_Structure:** dstruct_ScheduleManagement.CancelAppointmentResponse
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/ScheduleManagement/iface_ScheduleManagement.xml

---

## Schedulemanagement.Schedulemanagement.Findavailableappointments

**Service:** ScheduleManagement
**Operation:** FindAvailableAppointments
**Type:** Request-Response
**Request_Structure:** dstruct_ScheduleManagement.FindAvailableAppointments
**Response_Structure:** dstruct_ScheduleManagement.FindAvailableAppointmentsResponse
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/ScheduleManagement/iface_ScheduleManagement.xml

---

## Schedulemanagement.Schedulemanagement.Reserveappointment

**Service:** ScheduleManagement
**Operation:** ReserveAppointment
**Type:** Request-Response
**Request_Structure:** dstruct_ScheduleManagement.ReserveAppointment
**Response_Structure:** dstruct_ScheduleManagement.ReserveAppointmentResponse
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/ScheduleManagement/iface_ScheduleManagement.xml

---

## Wfm.Wfmresolutionintf.Ordercareresolution

**Service:** wfm Resolution Intf
**Operation:** OrderCareResolution
**Type:** Request-Response
**Request_Structure:** dstruct_WFM.OrderCareResolution
**Response_Structure:** dstruct_WFM.OrderCareResolutionAck
**Description:** Operation for the OrderCareResolution for WFM to EOC.
**File_Path:** Trunk/FrontierOM/metadata/WFM/iface_wfmResolutionIntf.xml

---

## Commonevolution.Consumeiaeventnotificationinterface.Consumeiaeventnotification

**Service:** consumeIAEventNotificationInterface
**Operation:** consumeIAEventNotification
**Type:** One-Way
**Request_Structure:** dstruct_commonEvolution.customerOrderChanged
**Response_Structure:** 
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/commonEvolution/iface_consumeIAEventNotificationInterface.xml

---

## Commonevolution.Procnotificationint.Processends

**Service:** procNotificationInt
**Operation:** processEnds
**Type:** Notification
**Request_Structure:** dstruct_commonEvolution.procNotification
**Response_Structure:** dstruct_commonEvolution.procNotification
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/commonEvolution/iface_procNotificationInt.xml

---

## Dataapi.Dataapiinterface.Getorderbyparameter

**Service:** dataAPIInterface
**Operation:** getOrderByParameter
**Type:** Request-Response
**Request_Structure:** dstruct_dataAPI.getOrderByParameterRequest
**Response_Structure:** dstruct_dataAPI.getOrderByParameterResponse
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/dataAPI/iface_dataAPIInterface.xml

---

## Dataapi.Dataapiinterface.Geteventlistbyorderid

**Service:** dataAPIInterface
**Operation:** getEventListByOrderId
**Type:** Request-Response
**Request_Structure:** dstruct_dataAPI.getEventListByOrderIdRequest
**Response_Structure:** dstruct_dataAPI.getEventListByOrderIdResponse
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/dataAPI/iface_dataAPIInterface.xml

---

## Dataapi.Dataapiinterface.Gettransactionlistbyorderid

**Service:** dataAPIInterface
**Operation:** getTransactionListByOrderId
**Type:** Request-Response
**Request_Structure:** dstruct_dataAPI.getTransactionListByOrderIdRequest
**Response_Structure:** dstruct_dataAPI.getTransactionListByOrderIdResponse
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/dataAPI/iface_dataAPIInterface.xml

---

## Httpinterfaces.Ifacilityservice.Getcurrentfacilities

**Service:** IFacilityService
**Operation:** GetCurrentFacilities
**Type:** Request-Response
**Request_Structure:** dstruct_httpInterfaces.httpRequest
**Response_Structure:** dstruct_httpInterfaces.httpResponse
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/httpInterfaces/iface_IFacilityService.xml

---

## Httpinterfaces.Dropshipservice.Createdropship

**Service:** dropShipService
**Operation:** createDropShip
**Type:** Request-Response
**Request_Structure:** dstruct_httpInterfaces.request
**Response_Structure:** dstruct_httpInterfaces.response
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/httpInterfaces/iface_dropShipService.xml

---

## Httpinterfaces.Provisioningservice.Loadsubscriber

**Service:** Provisioning Service
**Operation:** loadSubscriber
**Type:** Request-Response
**Request_Structure:** dstruct_httpInterfaces.httpRequest
**Response_Structure:** dstruct_httpInterfaces.httpResponse
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/httpInterfaces/iface_provisioningService.xml

---

## Httpinterfaces.Provisioningservice.Updatesubscriber

**Service:** Provisioning Service
**Operation:** updateSubscriber
**Type:** Request-Response
**Request_Structure:** dstruct_httpInterfaces.httpRequest
**Response_Structure:** dstruct_httpInterfaces.httpResponse
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/httpInterfaces/iface_provisioningService.xml

---

## Liw.Libnotification.Receivedcustomerresponse

**Service:** libNotification
**Operation:** receivedCustomerResponse
**Type:** Notification
**Request_Structure:** 
**Response_Structure:** 
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/liw/iface_libNotification.xml

---

## Ordercare.Installationconfiguration.Getinstalloption

**Service:** installationConfiguration
**Operation:** getInstallOption
**Type:** Request-Response
**Request_Structure:** dstruct_orderCare.InstallationConfigurationRequest
**Response_Structure:** dstruct_DT.tmf622ext.data.InstallationConfigurationResponse
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/orderCare/iface_installationConfiguration.xml

---

## Cpq.Services.Cpqcustomerordermanagement.Cancelcustomerorder

**Service:** CPQCustomerOrderManagement
**Operation:** CancelCustomerOrder
**Type:** Request-Response
**Request_Structure:** dstruct_CustomerOrderManagement.CancelCustomerOrder
**Response_Structure:** dstruct_CustomerOrderManagement.CancelCustomerOrderResponse
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/CPQ/Services/iface_CPQCustomerOrderManagement.xml

---

## Cpq.Services.Cpqcustomerordermanagement.Commitcustomerorder

**Service:** CPQCustomerOrderManagement
**Operation:** CommitCustomerOrder
**Type:** Request-Response
**Request_Structure:** dstruct_CustomerOrderManagement.CommitCustomerOrder
**Response_Structure:** dstruct_CustomerOrderManagement.CommitCustomerOrderResponse
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/CPQ/Services/iface_CPQCustomerOrderManagement.xml

---

## Cpq.Services.Cpqcustomerordermanagement.Submitcustomerorder

**Service:** CPQCustomerOrderManagement
**Operation:** SubmitCustomerOrder
**Type:** Request-Response
**Request_Structure:** dstruct_CustomerOrderManagement.SubmitCustomerOrder
**Response_Structure:** dstruct_CustomerOrderManagement.SubmitCustomerOrderResponse
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/CPQ/Services/iface_CPQCustomerOrderManagement.xml

---

## Cpq.Services.Cpqcustomerordermanagement.Updatecustomerorder

**Service:** CPQCustomerOrderManagement
**Operation:** UpdateCustomerOrder
**Type:** Request-Response
**Request_Structure:** dstruct_CustomerOrderManagement.UpdateCustomerOrder
**Response_Structure:** dstruct_CustomerOrderManagement.UpdateCustomerOrderResponse
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/CPQ/Services/iface_CPQCustomerOrderManagement.xml

---

## Cpq.Services.Confirmcustomerorder.Confirmcustomerorder

**Service:** confirmCustomerOrder
**Operation:** confirmCustomerOrder
**Type:** Request-Response
**Request_Structure:** dstruct_CPQ.Services.ConfirmRequest
**Response_Structure:** dstruct_CPQ.Services.ConfirmOrderResponse
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/CPQ/Services/iface_confirmCustomerOrder.xml

---

## Cpq.Services.Cpqorderserviceinter.Submitorder

**Service:** CPQ order Service Interface
**Operation:** SubmitOrder
**Type:** Request-Response
**Request_Structure:** dstruct_ManageOrder.ManageOrderSubmitOrderRequest
**Response_Structure:** dstruct_ManageOrder.ManageOrderSubmitOrderResponse
**Description:** Operation associated with the interface. This is a request-response interface.
**File_Path:** Trunk/FrontierOM/metadata/CPQ/Services/iface_cpqOrderServiceInter.xml

---

## Dt.Appointmentservices.Appointmentinterface.Cancelreservedapp

**Service:** appointmentInterface
**Operation:** cancelReservedApp
**Type:** Request-Response
**Request_Structure:** 
**Response_Structure:** dstruct_DT.appointmentServices.cancelReservedAppResponse
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/DT/appointmentServices/iface_appointmentInterface.xml

---

## Dt.Errorhandling.Errorhandlinginterface.Resume

**Service:** errorHandlingInterface
**Operation:** resume
**Type:** Notification
**Request_Structure:** 
**Response_Structure:** 
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/DT/errorHandling/iface_errorHandlingInterface.xml

---

## Dt.Errorhandling.Errorhandlinginterface.Rollback

**Service:** errorHandlingInterface
**Operation:** rollback
**Type:** Notification
**Request_Structure:** 
**Response_Structure:** 
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/DT/errorHandling/iface_errorHandlingInterface.xml

---

## Dt.Errorhandling.Errorhandlinginterface.Close

**Service:** errorHandlingInterface
**Operation:** close
**Type:** Notification
**Request_Structure:** 
**Response_Structure:** 
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/DT/errorHandling/iface_errorHandlingInterface.xml

---

## Dt.Errorhandling.Exceptionhandlerinterface.Skip

**Service:** exceptionHandlerInterface
**Operation:** skip
**Type:** Notification
**Request_Structure:** 
**Response_Structure:** 
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/DT/errorHandling/iface_exceptionHandlerInterface.xml

---

## Dt.Errorhandling.Exceptionhandlerinterface.Retry

**Service:** exceptionHandlerInterface
**Operation:** retry
**Type:** Notification
**Request_Structure:** 
**Response_Structure:** 
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/DT/errorHandling/iface_exceptionHandlerInterface.xml

---

## Dt.Errorhandling.Exceptionhandlerinterface.Onexception

**Service:** exceptionHandlerInterface
**Operation:** onException
**Type:** One-Way
**Request_Structure:** 
**Response_Structure:** 
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/DT/errorHandling/iface_exceptionHandlerInterface.xml

---

## Dt.Errorhandling.Wfmnotificationint.Resolution

**Service:** wfmNotificationInt
**Operation:** resolution
**Type:** Notification
**Request_Structure:** dstruct_DT.eventNotification.ErrorContextData
**Response_Structure:** 
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/DT/errorHandling/iface_wfmNotificationInt.xml

---

## Dt.Eventnotification.Consumedropeventnotificationinterface.Consumedropeventnotification

**Service:** consumeDropEventNotificationInterface
**Operation:** consumeDropEventNotification
**Type:** One-Way
**Request_Structure:** dstruct_DT.eventNotification.eventObject
**Response_Structure:** 
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/DT/eventNotification/iface_consumeDropEventNotificationInterface.xml

---

## Dt.Eventnotification.Consumeeventnotificationinterface.Consumenotification

**Service:** consumeEventNotificationInterface
**Operation:** consumeNotification
**Type:** One-Way
**Request_Structure:** dstruct_DT.eventNotification.eventObject
**Response_Structure:** 
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/DT/eventNotification/iface_consumeEventNotificationInterface.xml

---

## Dt.Eventnotification.Publisheventnotificationinterface.Publishnotification

**Service:** publishEventNotificationInterface
**Operation:** publishNotification
**Type:** Request-Response
**Request_Structure:** dstruct_DT.eventNotification.eventObject
**Response_Structure:** dstruct_DT.eventNotification.eventResponse
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/DT/eventNotification/iface_publishEventNotificationInterface.xml

---

## Dt.Manageorder.Dtesbnotification.Posted

**Service:** dtEsbNotification
**Operation:** posted
**Type:** Notification
**Request_Structure:** 
**Response_Structure:** 
**Description:** Notify the process of the Digital Transformation order is completed in DPI
**File_Path:** Trunk/FrontierOM/metadata/DT/manageOrder/iface_dtEsbNotification.xml

---

## Dt.Manageorder.Dtesbnotification.Substage

**Service:** dtEsbNotification
**Operation:** subStage
**Type:** Notification
**Request_Structure:** 
**Response_Structure:** 
**Description:** Notify the process reached sub stage.
**File_Path:** Trunk/FrontierOM/metadata/DT/manageOrder/iface_dtEsbNotification.xml

---

## Dt.Manageorder.Dtesbnotification.Cancel

**Service:** dtEsbNotification
**Operation:** cancel
**Type:** Notification
**Request_Structure:** 
**Response_Structure:** 
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/DT/manageOrder/iface_dtEsbNotification.xml

---

## Dt.Manageorder.Dtesbnotification.Eventassignmentcomplete

**Service:** dtEsbNotification
**Operation:** eventAssignmentComplete
**Type:** Notification
**Request_Structure:** 
**Response_Structure:** 
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/DT/manageOrder/iface_dtEsbNotification.xml

---

## Dt.Manageorder.Dtesbnotification.Csrrequest

**Service:** dtEsbNotification
**Operation:** csrRequest
**Type:** Notification
**Request_Structure:** 
**Response_Structure:** 
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/DT/manageOrder/iface_dtEsbNotification.xml

---

## Dt.Manageorder.Dtesbnotification.Terminateportautomation

**Service:** dtEsbNotification
**Operation:** terminatePortAutomation
**Type:** Notification
**Request_Structure:** 
**Response_Structure:** 
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/DT/manageOrder/iface_dtEsbNotification.xml

---

## Dt.Manageorder.Dtesbnotification.Lsrresponse

**Service:** dtEsbNotification
**Operation:** lsrResponse
**Type:** Notification
**Request_Structure:** 
**Response_Structure:** 
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/DT/manageOrder/iface_dtEsbNotification.xml

---

## Dt.Manageorder.Dtesbnotification.Heldpassed

**Service:** dtEsbNotification
**Operation:** heldPassed
**Type:** Notification
**Request_Structure:** 
**Response_Structure:** 
**Description:** Notify the process when the order passed held stage and cannot be put in hold in future.
**File_Path:** Trunk/FrontierOM/metadata/DT/manageOrder/iface_dtEsbNotification.xml

---

## Dt.Manageorder.Dtesbnotification.Updateorderduedate

**Service:** dtEsbNotification
**Operation:** updateOrderDueDate
**Type:** Notification
**Request_Structure:** 
**Response_Structure:** 
**Description:** Notify the process  OrderDueDate updated in DPI
**File_Path:** Trunk/FrontierOM/metadata/DT/manageOrder/iface_dtEsbNotification.xml

---

## Dt.Manageorder.Dtesbnotification.Ended

**Service:** dtEsbNotification
**Operation:** ended
**Type:** Notification
**Request_Structure:** 
**Response_Structure:** 
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/DT/manageOrder/iface_dtEsbNotification.xml

---

## Dt.Manageorder.Dtesbnotification.Tosstage

**Service:** dtEsbNotification
**Operation:** tosStage
**Type:** Notification
**Request_Structure:** 
**Response_Structure:** 
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/DT/manageOrder/iface_dtEsbNotification.xml

---

## Dt.Manageorder.Dtesbnotification.Receivedtoscustomerack

**Service:** dtEsbNotification
**Operation:** receivedTOSCustomerAck
**Type:** Notification
**Request_Structure:** 
**Response_Structure:** 
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/DT/manageOrder/iface_dtEsbNotification.xml

---

## Dt.Manageorder.Dtesbnotification.Tosendstage

**Service:** dtEsbNotification
**Operation:** tosEndStage
**Type:** Notification
**Request_Structure:** 
**Response_Structure:** 
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/DT/manageOrder/iface_dtEsbNotification.xml

---

## Dt.Manageorder.Dtnotification.Update

**Service:** Digital Transformation Internal Interface
**Operation:** update
**Type:** Notification
**Request_Structure:** 
**Response_Structure:** 
**Description:** Notify the process of the Digital Transformation order update
**File_Path:** Trunk/FrontierOM/metadata/DT/manageOrder/iface_dtNotification.xml

---

## Dt.Manageorder.Dtnotification.Cancel

**Service:** Digital Transformation Internal Interface
**Operation:** cancel
**Type:** Notification
**Request_Structure:** 
**Response_Structure:** 
**Description:** Notify the process of the Digital Transformation order cancellation
**File_Path:** Trunk/FrontierOM/metadata/DT/manageOrder/iface_dtNotification.xml

---

## Dt.Manageorder.Dtnotification.Updatedate

**Service:** Digital Transformation Internal Interface
**Operation:** updateDate
**Type:** Notification
**Request_Structure:** 
**Response_Structure:** 
**Description:** Notify the process of the Digital Transformation order updated date
**File_Path:** Trunk/FrontierOM/metadata/DT/manageOrder/iface_dtNotification.xml

---

## Dt.Orderstatus.Omstatusinterface.Getstatus

**Service:** omStatusInterface
**Operation:** getStatus
**Type:** Request-Response
**Request_Structure:** 
**Response_Structure:** dstruct_DT.orderStatus.orderStatus
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/DT/orderStatus/iface_omStatusInterface.xml

---

## Dt.Pega.Servicecase.Updateservicecase

**Service:** servicecase
**Operation:** updateServicecase
**Type:** Request-Response
**Request_Structure:** dstruct_DT.pega.updateServiceCaseRequest
**Response_Structure:** dstruct_DT.pega.updateServiceCaseResponse
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/DT/pega/iface_servicecase.xml

---

## Dt.Scheduleappointment.Ossschedules.Put Schedulechangenotification

**Service:** OssSchedules
**Operation:** PUT_ScheduleChangeNotification
**Type:** Request-Response
**Request_Structure:** dstruct_DT.scheduleAppointment.PUT_ScheduleChangeNotification_InputMessage
**Response_Structure:** dstruct_DT.scheduleAppointment.ScheduleChangeNotificationResponse
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/DT/scheduleAppointment/iface_OssSchedules.xml

---

## Dt.Scheduleappointment.Ossschedules.Getduedate

**Service:** OssSchedules
**Operation:** getDueDate
**Type:** Request-Response
**Request_Structure:** 
**Response_Structure:** dstruct_DT.scheduleAppointment.getDueDateResponse
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/DT/scheduleAppointment/iface_OssSchedules.xml

---

## Dt.Termsofservice.Osstos.Getcustomertos

**Service:** ossTos
**Operation:** getCustomerTos
**Type:** Request-Response
**Request_Structure:** dstruct_om.data.genericRequest
**Response_Structure:** dstruct_DT.termsOfService.getCustomerTosResponse
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/DT/termsOfService/iface_ossTos.xml

---

## Dt.Termsofservice.Osstos.Updatecustomertos

**Service:** ossTos
**Operation:** updateCustomerToS
**Type:** Request-Response
**Request_Structure:** dstruct_om.data.genericRequest
**Response_Structure:** dstruct_DT.termsOfService.updateToS
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/DT/termsOfService/iface_ossTos.xml

---

## Dt.Treatmentmanagement.Treatmentmanagement.Createcustomeraccountredflags

**Service:** TreatmentManagement
**Operation:** CreateCustomerAccountRedFlags
**Type:** Request-Response
**Request_Structure:** dstruct_DT.treatmentManagement.CreateCustomerAccountRedFlags
**Response_Structure:** dstruct_DT.treatmentManagement.CreateCustomerAccountRedFlagsResponse
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/DT/treatmentManagement/iface_TreatmentManagement.xml

---

## Dt.Treatmentmanagement.Treatmentmanagement.Updatecustomeraccountredflag

**Service:** TreatmentManagement
**Operation:** UpdateCustomerAccountRedFlag
**Type:** Request-Response
**Request_Structure:** dstruct_DT.treatmentManagement.UpdateCustomerAccountRedFlag
**Response_Structure:** dstruct_DT.treatmentManagement.UpdateCustomerAccountRedFlagResponse
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/DT/treatmentManagement/iface_TreatmentManagement.xml

---

## Dt.Vxfield.Vffield.Create

**Service:** vfField
**Operation:** create
**Type:** Request-Response
**Request_Structure:** 
**Response_Structure:** 
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/DT/vxField/iface_vfField.xml

---

## Dt.Vxfield.Vffield.Cancel

**Service:** vfField
**Operation:** cancel
**Type:** Request-Response
**Request_Structure:** 
**Response_Structure:** 
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/DT/vxField/iface_vfField.xml

---

## Dt.Vxfield.Vffield.Update

**Service:** vfField
**Operation:** update
**Type:** Request-Response
**Request_Structure:** 
**Response_Structure:** 
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/DT/vxField/iface_vfField.xml

---

## Interfaces.Bobo.Subscriptions.Addsubscriptiontoaccount

**Service:** Subscriptions
**Operation:** addSubscriptionToAccount
**Type:** Request-Response
**Request_Structure:** dstruct_Interfaces.BOBO.addSubscriptionRequest
**Response_Structure:** dstruct_Interfaces.BOBO.addSubscriptionResponse
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/Interfaces/BOBO/iface_Subscriptions.xml

---

## Interfaces.Bobo.Subscriptions V2.Addsubscriptiontoaccount

**Service:** Subscriptions_v2
**Operation:** addSubscriptionToAccount
**Type:** Request-Response
**Request_Structure:** dstruct_Interfaces.BOBO.addSubscriptionRequest
**Response_Structure:** dstruct_Interfaces.BOBO.addSubscriptionResponse
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/Interfaces/BOBO/iface_Subscriptions_v2.xml

---

## Interfaces.Capillary.Capillaryapi.Membercreation

**Service:** capillaryapi
**Operation:** membercreation
**Type:** Request-Response
**Request_Structure:** dstruct_Interfaces.Capillary.CreateMemberRequest
**Response_Structure:** dstruct_Interfaces.Capillary.CreateMemberResponse
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/Interfaces/Capillary/iface_capillaryapi.xml

---

## Interfaces.Eero.Eeroinitiate.Movein

**Service:** eeroInitiate
**Operation:** moveIn
**Type:** Request-Response
**Request_Structure:** dstruct_Interfaces.EERO.moveInRequest
**Response_Structure:** dstruct_Interfaces.EERO.response
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/Interfaces/EERO/iface_eeroInitiate.xml

---

## Interfaces.Eero.Eeroinitiate.Moveout

**Service:** eeroInitiate
**Operation:** moveOut
**Type:** Request-Response
**Request_Structure:** dstruct_Interfaces.EERO.moveOutRequest
**Response_Structure:** dstruct_Interfaces.EERO.response
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/Interfaces/EERO/iface_eeroInitiate.xml

---

## Interfaces.Soa.Updatefocdateforsoa.Soaupdatefocdate

**Service:** updateFocDateForSoa
**Operation:** soaUpdateFocDate
**Type:** Request-Response
**Request_Structure:** dstruct_Interfaces.SOA.updateFocDate
**Response_Structure:** dstruct_Interfaces.SOA.soaResponse
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/Interfaces/SOA/iface_updateFocDateForSoa.xml

---

## Interfaces.Common.Oauth.Get Accesstoken

**Service:** oauth
**Operation:** GET_accesstoken
**Type:** Request-Response
**Request_Structure:** 
**Response_Structure:** dstruct_Interfaces.common.AccessTokenResponse
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/Interfaces/common/iface_oauth.xml

---

## Interfaces.Vxfield.Callgatewayinterface.Createprefield

**Service:** callGatewayInterface
**Operation:** createPrefield
**Type:** Request-Response
**Request_Structure:** dstruct_Interfaces.vxField.CreatePrefieldRequest
**Response_Structure:** dstruct_Interfaces.vxField.CreatePrefieldResponse
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/Interfaces/vxField/iface_callGatewayInterface.xml

---

## Ldap.Tests.Verifyuserserviceint.Verifyuser

**Service:** verifyUserServiceInt
**Operation:** verifyUser
**Type:** Request-Response
**Request_Structure:** dstruct_cwf.ldapSearchCriteria
**Response_Structure:** dstruct_cwf.ldapEntryArray
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/LDAP/Tests/iface_verifyUserServiceInt.xml

---

## Ringcentral.Rc.Rcshippinglocation.Get Eocshippingdetails

**Service:** RCShippingLocation
**Operation:** GET_EOCShippingDetails
**Type:** Request-Response
**Request_Structure:** 
**Response_Structure:** dstruct_RingCentral.RC.eocShippingDetailsResponse
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/RingCentral/RC/iface_RCShippingLocation.xml

---

## Ringcentral.Rc.Ringcentral.Post Initialorder

**Service:** RingCentral
**Operation:** POST_InitialOrder
**Type:** Request-Response
**Request_Structure:** dstruct_RingCentral.RC.initialOrderRequest
**Response_Structure:** dstruct_RingCentral.RC.initialOrderResponse
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/RingCentral/RC/iface_RingCentral.xml

---

## Ringcentral.Rc.Ringcentral.Get Partnertoken

**Service:** RingCentral
**Operation:** GET_PartnerToken
**Type:** Request-Response
**Request_Structure:** 
**Response_Structure:** dstruct_RingCentral.RC.tokenResponse
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/RingCentral/RC/iface_RingCentral.xml

---

## Ringcentral.Rc.Ringcentral.Get Accounttoken

**Service:** RingCentral
**Operation:** GET_AccountToken
**Type:** Request-Response
**Request_Structure:** 
**Response_Structure:** dstruct_RingCentral.RC.tokenResponse
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/RingCentral/RC/iface_RingCentral.xml

---

## Ringcentral.Rc.Ringcentral.Post Deviceorder

**Service:** RingCentral
**Operation:** POST_DeviceOrder
**Type:** Request-Response
**Request_Structure:** dstruct_RingCentral.RC.deviceOrderRequest
**Response_Structure:** dstruct_RingCentral.RC.deviceOrderResponse
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/RingCentral/RC/iface_RingCentral.xml

---

## Ringcentral.Rc.Ringcentral.Patch Accountstatus

**Service:** RingCentral
**Operation:** PATCH_AccountStatus
**Type:** Request-Response
**Request_Structure:** dstruct_RingCentral.RC.patchUpdateAccountStatusRequest
**Response_Structure:** dstruct_RingCentral.RC.patchUpdateAccountStatusResponse
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/RingCentral/RC/iface_RingCentral.xml

---

## Ringcentral.Rc.Ringcentral.Delete Account

**Service:** RingCentral
**Operation:** DELETE_Account
**Type:** Request-Response
**Request_Structure:** dstruct_RingCentral.RC.genericRequest
**Response_Structure:** 
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/RingCentral/RC/iface_RingCentral.xml

---

## Ringcentral.Rc.Ringcentral.Post Licensesprovision

**Service:** RingCentral
**Operation:** POST_LicensesProvision
**Type:** Request-Response
**Request_Structure:** dstruct_RingCentral.RC.licensesProvisionRequest
**Response_Structure:** dstruct_RingCentral.RC.genericResponse
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/RingCentral/RC/iface_RingCentral.xml

---

## Ringcentral.Rc.Ringcentral.Get Extensionlist

**Service:** RingCentral
**Operation:** GET_ExtensionList
**Type:** Request-Response
**Request_Structure:** dstruct_RingCentral.RC.genericRequest
**Response_Structure:** dstruct_RingCentral.RC.genericResponse
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/RingCentral/RC/iface_RingCentral.xml

---

## Ringcentral.Rc.Ringcentral.Post Upgradeaccount

**Service:** RingCentral
**Operation:** POST_UpgradeAccount
**Type:** Request-Response
**Request_Structure:** dstruct_RingCentral.RC.genericRequest
**Response_Structure:** dstruct_RingCentral.RC.genericResponse
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/RingCentral/RC/iface_RingCentral.xml

---

## Swc.Ossplantfacility.Ossplantfacility.Dropdetails

**Service:** ossPlantFacility
**Operation:** dropDetails
**Type:** Request-Response
**Request_Structure:** 
**Response_Structure:** dstruct_SWC.OssPlantFacility.DropDetailsResponse
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/SWC/OssPlantFacility/iface_ossPlantFacility.xml

---

## Swc.Vxfield.Dropcall.Createdropcall

**Service:** dropCall
**Operation:** createDropCall
**Type:** Request-Response
**Request_Structure:** dstruct_SWC.VxField.DropCallRequest
**Response_Structure:** dstruct_SWC.VxField.VxFieldResponse
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/SWC/VxField/iface_dropCall.xml

---

## Swc.Vxfield.Dropcall.Updatedropcall

**Service:** dropCall
**Operation:** updateDropCall
**Type:** Request-Response
**Request_Structure:** dstruct_SWC.VxField.DropCallRequest
**Response_Structure:** dstruct_SWC.VxField.VxFieldResponse
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/SWC/VxField/iface_dropCall.xml

---

## Swc.Vxfield.Dropcall.Reportmessage

**Service:** dropCall
**Operation:** reportMessage
**Type:** Request-Response
**Request_Structure:** dstruct_SWC.VxField.ReportMessageRequest
**Response_Structure:** dstruct_SWC.VxField.VxFieldResponse
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/SWC/VxField/iface_dropCall.xml

---

## Commonevolution.Errorhandling.Interfaceexceptionhandlerint.Skip

**Service:** interfaceExceptionHandlerInt
**Operation:** skip
**Type:** Notification
**Request_Structure:** 
**Response_Structure:** 
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/commonEvolution/errorHandling/iface_interfaceExceptionHandlerInt.xml

---

## Commonevolution.Errorhandling.Interfaceexceptionhandlerint.Retry

**Service:** interfaceExceptionHandlerInt
**Operation:** retry
**Type:** Notification
**Request_Structure:** 
**Response_Structure:** 
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/commonEvolution/errorHandling/iface_interfaceExceptionHandlerInt.xml

---

## Commonevolution.Errorhandling.Interfaceexceptionhandlerint.Onexception

**Service:** interfaceExceptionHandlerInt
**Operation:** onException
**Type:** One-Way
**Request_Structure:** 
**Response_Structure:** 
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/commonEvolution/errorHandling/iface_interfaceExceptionHandlerInt.xml

---

## Commonevolution.Errorhandling.Processexceptionhandlerint.Skip

**Service:** processExceptionHandlerInt
**Operation:** skip
**Type:** Notification
**Request_Structure:** 
**Response_Structure:** 
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/commonEvolution/errorHandling/iface_processExceptionHandlerInt.xml

---

## Commonevolution.Errorhandling.Processexceptionhandlerint.Retry

**Service:** processExceptionHandlerInt
**Operation:** retry
**Type:** Notification
**Request_Structure:** 
**Response_Structure:** 
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/commonEvolution/errorHandling/iface_processExceptionHandlerInt.xml

---

## Commonevolution.Errorhandling.Processexceptionhandlerint.Onexception

**Service:** processExceptionHandlerInt
**Operation:** onException
**Type:** One-Way
**Request_Structure:** 
**Response_Structure:** 
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/commonEvolution/errorHandling/iface_processExceptionHandlerInt.xml

---

## Commonevolution.Errorhandling.Wsdlexceptionhandlerint.Skip

**Service:** wsdlExceptionHandlerInt
**Operation:** skip
**Type:** Notification
**Request_Structure:** 
**Response_Structure:** 
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/commonEvolution/errorHandling/iface_wsdlExceptionHandlerInt.xml

---

## Commonevolution.Errorhandling.Wsdlexceptionhandlerint.Retry

**Service:** wsdlExceptionHandlerInt
**Operation:** retry
**Type:** Notification
**Request_Structure:** 
**Response_Structure:** 
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/commonEvolution/errorHandling/iface_wsdlExceptionHandlerInt.xml

---

## Commonevolution.Errorhandling.Wsdlexceptionhandlerint.Onexception

**Service:** wsdlExceptionHandlerInt
**Operation:** onException
**Type:** One-Way
**Request_Structure:** 
**Response_Structure:** 
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/commonEvolution/errorHandling/iface_wsdlExceptionHandlerInt.xml

---

## Ordercare.Opa.Coreservices.Getcoreservices

**Service:** coreServices
**Operation:** getCoreServices
**Type:** Request-Response
**Request_Structure:** 
**Response_Structure:** dstruct_orderCare.OPA.response
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/orderCare/OPA/iface_coreServices.xml

---

## Ordercare.Rg.Residentialgateways.Getresidentialgateways

**Service:** residentialgateways
**Operation:** getResidentialgateways
**Type:** Request-Response
**Request_Structure:** dstruct_orderCare.RG.getResidentialgatewaysResponse
**Response_Structure:** dstruct_orderCare.RG.getResidentialgatewaysResponse
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/orderCare/RG/iface_residentialgateways.xml

---

## Ordercare.Usi.Dpivalence.Getaccountidentificationinformation

**Service:** dpiValence
**Operation:** getAccountIdentificationInformation
**Type:** Request-Response
**Request_Structure:** 
**Response_Structure:** dstruct_orderCare.USI.response
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/orderCare/USI/iface_dpiValence.xml

---

## Provisioningservicephase2.Customerorderconfirmation.Customerorderconfirmationemailintf.Customerorderconfirmationemail

**Service:** customerOrderConfirmationEmailIntf
**Operation:** customerOrderConfirmationEmail
**Type:** Request-Response
**Request_Structure:** dstruct_provisioningServicePhase2.CustomerOrderConfirmation.customerOrderConfirmationEmailRequest
**Response_Structure:** dstruct_provisioningServicePhase2.CustomerOrderConfirmation.customerOrderConfirmationEmailResponse
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/provisioningServicePhase2/CustomerOrderConfirmation/iface_customerOrderConfirmationEmailIntf.xml

---

## Provisioningservicephase2.Customerordermanagement.Determinerequiredprovinterface.Determinerequiredprovisioning

**Service:** DetermineRequiredProvInterface
**Operation:** determineRequiredProvisioning
**Type:** Request-Response
**Request_Structure:** dstruct_provisioningServicePhase2.CustomerOrderManagement.determineRequiredProvisioningDS.rest_DetermineRequiredProvisioningRequest
**Response_Structure:** dstruct_provisioningServicePhase2.CustomerOrderManagement.determineRequiredProvisioningDS.response
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/provisioningServicePhase2/CustomerOrderManagement/iface_DetermineRequiredProvInterface.xml

---

## Provisioningservicephase2.Customerordermanagement.Provisionorderbyinterface.Initiateprovisioning

**Service:** ProvisionOrderByInterface
**Operation:** InitiateProvisioning
**Type:** Request-Response
**Request_Structure:** dstruct_provisioningServicePhase2.CustomerOrderManagement.provisioningRequest
**Response_Structure:** dstruct_provisioningServicePhase2.CustomerOrderManagement.provisioningResponse
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/provisioningServicePhase2/CustomerOrderManagement/iface_ProvisionOrderByInterface.xml

---

## Provisioningservicephase2.Customerordermanagement.Receivedpinotifications.Receivecancelnotifications

**Service:** ReceiveDPINotifications
**Operation:** receiveCancelNotifications
**Type:** Request-Response
**Request_Structure:** dstruct_provisioningServicePhase2.CustomerOrderManagement.root
**Response_Structure:** dstruct_provisioningServicePhase2.CustomerOrderManagement.root
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/provisioningServicePhase2/CustomerOrderManagement/iface_ReceiveDPINotifications.xml

---

## Provisioningservicephase2.Customerordermanagement.Receiveemsnotification.Customerorderstagedtoocnotification

**Service:** ReceiveEMSNotification
**Operation:** customerOrderStagedToOCNotification
**Type:** Request-Response
**Request_Structure:** dstruct_provisioningServicePhase2.CustomerOrderManagement.CustomerOrderStagedToOC
**Response_Structure:** dstruct_provisioningServicePhase2.CustomerOrderManagement.CustomerOrderStagedToOC
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/provisioningServicePhase2/CustomerOrderManagement/iface_ReceiveEMSNotification.xml

---

## Provisioningservicephase2.Customerordermanagement.Receiveerrornotificationintf.Errornotification

**Service:** ReceiveErrorNotificationIntf
**Operation:** errorNotification
**Type:** Request-Response
**Request_Structure:** dstruct_WFM.OrderCareResolution
**Response_Structure:** dstruct_WFM.OrderCareResolution
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/provisioningServicePhase2/CustomerOrderManagement/iface_ReceiveErrorNotificationIntf.xml

---

## Provisioningservicephase2.Customerordermanagement.Receiveprovisioningnotifications.Receiveprovnotifications

**Service:** ReceiveProvisioningNotifications
**Operation:** ReceiveProvNotifications
**Type:** One-Way
**Request_Structure:** dstruct_provisioningServicePhase2.CustomerOrderManagement.provisioningSystemCompletedEvent
**Response_Structure:** dstruct_provisioningServicePhase2.CustomerOrderManagement.provisioningSystemCompletedEvent
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/provisioningServicePhase2/CustomerOrderManagement/iface_ReceiveProvisioningNotifications.xml

---

## Provisioningservicephase2.Customerordermanagement.Receivestagecodechangednotification.Customerorderstagecodechangednotification

**Service:** ReceiveStageCodeChangedNotification
**Operation:** customerOrderStageCodeChangedNotification
**Type:** Notification
**Request_Structure:** dstruct_provisioningServicePhase2.CustomerOrderManagement.CustomerOrderStageCodeChangedEvent
**Response_Structure:** dstruct_provisioningServicePhase2.CustomerOrderManagement.CustomerOrderStageCodeChangedEvent
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/provisioningServicePhase2/CustomerOrderManagement/iface_ReceiveStageCodeChangedNotification.xml

---

## Provisioningservicephase2.Customerordermanagement.Stagecodeinterface.Setstagecode

**Service:** stageCodeInterface
**Operation:** setStageCode
**Type:** Request-Response
**Request_Structure:** dstruct_provisioningServicePhase2.CustomerOrderManagement.request
**Response_Structure:** dstruct_provisioningServicePhase2.CustomerOrderManagement.response
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/provisioningServicePhase2/CustomerOrderManagement/iface_stageCodeInterface.xml

---

## Dt.Tmf622Ext.Service.Installationconfiguration.Getinstalloption

**Service:** installationConfiguration
**Operation:** getInstallOption
**Type:** Request-Response
**Request_Structure:** dstruct_DT.tmf622ext.data.installOptionRequest
**Response_Structure:** dstruct_DT.tmf622ext.data.installOptionDTResponse
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/DT/tmf622ext/service/iface_installationConfiguration.xml

---

## Dt.Tmf622Ext.Service.Ominterface.Createorder

**Service:** omInterface
**Operation:** createOrder
**Type:** Request-Response
**Request_Structure:** dstruct_DT.tmf622ext.dataSpec.QuoteToOrderRequest
**Response_Structure:** dstruct_DT.tmf622ext.dataSpec.QuoteToOrderResponse
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/DT/tmf622ext/service/iface_omInterface.xml

---

## Dt.Tmf622Ext.Service.Ominterface.Updateorder

**Service:** omInterface
**Operation:** updateOrder
**Type:** Request-Response
**Request_Structure:** dstruct_DT.tmf622ext.dataSpec.QuoteToOrderRequest
**Response_Structure:** dstruct_DT.tmf622ext.dataSpec.QuoteToOrderResponse
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/DT/tmf622ext/service/iface_omInterface.xml

---

## Dt.Tmf622Ext.Service.Ominterface.Getorder

**Service:** omInterface
**Operation:** getOrder
**Type:** Request-Response
**Request_Structure:** 
**Response_Structure:** dstruct_DT.tmf622ext.dataSpec.GetQuoteResponse
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/DT/tmf622ext/service/iface_omInterface.xml

---

## Dt.Tmf622Ext.Service.Ominterface.Cancelorder

**Service:** omInterface
**Operation:** cancelOrder
**Type:** Request-Response
**Request_Structure:** 
**Response_Structure:** dstruct_DT.tmf622ext.dataSpec.QuoteToOrderResponse
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/DT/tmf622ext/service/iface_omInterface.xml

---

## Interfaces.Bss.Orderapi.Ordersummaries.Customerorderdetails

**Service:** OrderSummaries
**Operation:** CustomerOrderDetails
**Type:** Request-Response
**Request_Structure:** dstruct_om.data.genericRequest
**Response_Structure:** dstruct_Interfaces.BSS.OrderApi.orderDetailsResponse
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/Interfaces/BSS/OrderApi/iface_OrderSummaries.xml

---

## Interfaces.Css.Myfrontieradmin.Accountattributes.Createaccountattribute

**Service:** AccountAttributes
**Operation:** createAccountAttribute
**Type:** Request-Response
**Request_Structure:** dstruct_Interfaces.CSS.MyFrontierAdmin.createAccountAttributeRequest
**Response_Structure:** dstruct_Interfaces.CSS.MyFrontierAdmin.createAccountAttributesResponse
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/Interfaces/CSS/MyFrontierAdmin/iface_AccountAttributes.xml

---

## Interfaces.Css.Customerattributes.Accounts.Createaccountattribute

**Service:** Accounts
**Operation:** createAccountAttribute
**Type:** Request-Response
**Request_Structure:** dstruct_Interfaces.CSS.customerAttributes.createAccountAttributeRequest
**Response_Structure:** dstruct_Interfaces.CSS.customerAttributes.accountAttributeResponse
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/Interfaces/CSS/customerAttributes/iface_Accounts.xml

---

## Interfaces.Css.Customerattributes.Accounts.Getaccountattribute

**Service:** Accounts
**Operation:** getAccountAttribute
**Type:** Request-Response
**Request_Structure:** 
**Response_Structure:** dstruct_Interfaces.CSS.customerAttributes.accountAttributeResponse
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/Interfaces/CSS/customerAttributes/iface_Accounts.xml

---

## Interfaces.Css.Customerattributes.Accounts.Getaccountattributebyattributeid

**Service:** Accounts
**Operation:** GetAccountAttributeByAttributeId
**Type:** Request-Response
**Request_Structure:** 
**Response_Structure:** dstruct_Interfaces.CSS.customerAttributes.accountAttributeResponse
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/Interfaces/CSS/customerAttributes/iface_Accounts.xml

---

## Interfaces.Dpi.Customer.Coreservicesinterface.Getcoreservicesbyusi

**Service:** coreservicesInterface
**Operation:** getCoreservicesByusi
**Type:** Request-Response
**Request_Structure:** 
**Response_Structure:** dstruct_Interfaces.DPI.Customer.coreservicesResponse
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/Interfaces/DPI/Customer/iface_coreservicesInterface.xml

---

## Interfaces.Dpi.Customer.Customeraccountidsinterface.Accountidsbyphonenumber

**Service:** customerAccountidsInterface
**Operation:** accountidsByphonenumber
**Type:** Request-Response
**Request_Structure:** 
**Response_Structure:** dstruct_Interfaces.DPI.Customer.response
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/Interfaces/DPI/Customer/iface_customerAccountidsInterface.xml

---

## Interfaces.Dpi.Product.Productsinterface.Customerproducts

**Service:** productsInterface
**Operation:** customerproducts
**Type:** Request-Response
**Request_Structure:** dstruct_om.data.genericRequest
**Response_Structure:** dstruct_Interfaces.DPI.Product.getProductsResponse
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/Interfaces/DPI/Product/iface_productsInterface.xml

---

## Interfaces.Dpi.Provisioning.Ossplantprovisioninginterface.Getprovisioningcodes

**Service:** ossplantprovisioningInterface
**Operation:** getProvisioningcodes
**Type:** Request-Response
**Request_Structure:** 
**Response_Structure:** dstruct_Interfaces.DPI.Provisioning.provisioningcodes
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/Interfaces/DPI/Provisioning/iface_ossplantprovisioningInterface.xml

---

## Interfaces.Esb.Esbbusinessrulesengine.Disclosures.Requireddisclosures

**Service:** Disclosures
**Operation:** requiredDisclosures
**Type:** Request-Response
**Request_Structure:** dstruct_Interfaces.ESB.EsbBusinessRulesEngine.requiredDisclosuresRequest
**Response_Structure:** dstruct_Interfaces.ESB.EsbBusinessRulesEngine.requiredDisclosuresResponse
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/Interfaces/ESB/EsbBusinessRulesEngine/iface_Disclosures.xml

---

## Interfaces.Esb.Esbpayments.Autopayment.Getautopaymentbyuuid

**Service:** autoPayment
**Operation:** getAutoPaymentByUUID
**Type:** Request-Response
**Request_Structure:** 
**Response_Structure:** dstruct_Interfaces.ESB.EsbPayments.autoPaymentsDS
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/Interfaces/ESB/EsbPayments/iface_autoPayment.xml

---

## Interfaces.Esb.Esbpayments.Walletfundingaccounts.Getfundingaccountsbyuuid

**Service:** walletFundingAccounts
**Operation:** getFundingAccountsByUUID
**Type:** Request-Response
**Request_Structure:** 
**Response_Structure:** dstruct_Interfaces.ESB.EsbPayments.fundingAccountsDS
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/Interfaces/ESB/EsbPayments/iface_walletFundingAccounts.xml

---

## Interfaces.Oss.Bng.Gateways.Getipdetails

**Service:** gateways
**Operation:** getIpdetails
**Type:** Request-Response
**Request_Structure:** 
**Response_Structure:** dstruct_Interfaces.OSS.Bng.ipdetailsResponse
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/Interfaces/OSS/Bng/iface_gateways.xml

---

## Interfaces.Oss.Bng.Gateways.Getbngstatusbyont

**Service:** gateways
**Operation:** getBNGStatusByONT
**Type:** Request-Response
**Request_Structure:** 
**Response_Structure:** dstruct_Interfaces.OSS.Bng.bngStatusByONTResponse
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/Interfaces/OSS/Bng/iface_gateways.xml

---

## Interfaces.Oss.Cpe.Equipment.Getequipmentbylocationid

**Service:** equipment
**Operation:** getEquipmentByLocationId
**Type:** Request-Response
**Request_Structure:** 
**Response_Structure:** dstruct_Interfaces.OSS.Cpe.equipmentByLocationIdResponse
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/Interfaces/OSS/Cpe/iface_equipment.xml

---

## Interfaces.Oss.Cpe.Equipment.Equipmentassociatebyserialnumber

**Service:** equipment
**Operation:** equipmentAssociateBySerialNumber
**Type:** Request-Response
**Request_Structure:** dstruct_Interfaces.OSS.Cpe.associateMeshDeviceRequest
**Response_Structure:** dstruct_Interfaces.OSS.Cpe.associateMeshDeviceResponse
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/Interfaces/OSS/Cpe/iface_equipment.xml

---

## Interfaces.Oss.Cpe.Equipment.Equipmentdisassociatebyserialnumber

**Service:** equipment
**Operation:** equipmentDisassociateBySerialNumber
**Type:** Request-Response
**Request_Structure:** dstruct_Interfaces.OSS.Cpe.associateMeshDeviceRequest
**Response_Structure:** dstruct_Interfaces.OSS.Cpe.equipmentDs
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/Interfaces/OSS/Cpe/iface_equipment.xml

---

## Interfaces.Oss.Cpe.Equipment.Equipmentdeactivatebyserialnumber

**Service:** equipment
**Operation:** equipmentDeactivateBySerialNumber
**Type:** Request-Response
**Request_Structure:** 
**Response_Structure:** dstruct_Interfaces.OSS.Cpe.equipmentDs
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/Interfaces/OSS/Cpe/iface_equipment.xml

---

## Interfaces.Oss.Cpe.Equipment.Equipmentactivatebyserialnumber

**Service:** equipment
**Operation:** equipmentActivateBySerialNumber
**Type:** Request-Response
**Request_Structure:** 
**Response_Structure:** dstruct_Interfaces.OSS.Cpe.equipmentDs
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/Interfaces/OSS/Cpe/iface_equipment.xml

---

## Interfaces.Oss.Cpe.Equipment.Getequipmentbyusi

**Service:** equipment
**Operation:** getEquipmentByUSI
**Type:** Request-Response
**Request_Structure:** 
**Response_Structure:** dstruct_Interfaces.OSS.Cpe.equipmentByUSIResponse
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/Interfaces/OSS/Cpe/iface_equipment.xml

---

## Interfaces.Oss.Cpe.Meshdevices.Getmeshdevicesbyserialnumber

**Service:** meshDevices
**Operation:** getMeshDevicesBySerialNumber
**Type:** Request-Response
**Request_Structure:** 
**Response_Structure:** dstruct_Interfaces.OSS.Cpe.meshDevicesBySerialNumberResponse
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/Interfaces/OSS/Cpe/iface_meshDevices.xml

---

## Interfaces.Oss.Cpe.Meshdevices.Getnetworkdetailsbyid

**Service:** meshDevices
**Operation:** getNetworkDetailsById
**Type:** Request-Response
**Request_Structure:** 
**Response_Structure:** dstruct_Interfaces.OSS.Cpe.networkDetailsByIdResponse
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/Interfaces/OSS/Cpe/iface_meshDevices.xml

---

## Interfaces.Oss.Cpe.Meshdevices.Meshdevicesdisassociatebyserialnumber

**Service:** meshDevices
**Operation:** meshDevicesDisassociateBySerialNumber
**Type:** Request-Response
**Request_Structure:** dstruct_Interfaces.OSS.Cpe.disAssociateMeshDeviceRequest
**Response_Structure:** dstruct_Interfaces.OSS.Cpe.associateMeshDeviceResponse
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/Interfaces/OSS/Cpe/iface_meshDevices.xml

---

## Interfaces.Oss.Customereligibility.Customereligibility.Getdiscounteligibility

**Service:** CustomerEligibility
**Operation:** getDiscountEligibility
**Type:** Request-Response
**Request_Structure:** 
**Response_Structure:** dstruct_Interfaces.OSS.CustomerEligibility.getDiscountEligibilityResponse
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/Interfaces/OSS/CustomerEligibility/iface_CustomerEligibility.xml

---

## Interfaces.Oss.Facilities.Ossfacilities.Getfacilities

**Service:** OSSFacilities
**Operation:** getFacilities
**Type:** Request-Response
**Request_Structure:** 
**Response_Structure:** dstruct_Interfaces.OSS.Facilities.GetFacilitiesResponse
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/Interfaces/OSS/Facilities/iface_OSSFacilities.xml

---

## Interfaces.Oss.Inventory.Equipment.Getequipmentbyusi

**Service:** equipment
**Operation:** getEquipmentByUSI
**Type:** Request-Response
**Request_Structure:** 
**Response_Structure:** dstruct_Interfaces.OSS.Inventory.equipmentsResponse
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/Interfaces/OSS/Inventory/iface_equipment.xml

---

## Interfaces.Oss.Inventory.Locations.Getequipmentbylocationid

**Service:** locations
**Operation:** getEquipmentByLocationId
**Type:** Request-Response
**Request_Structure:** 
**Response_Structure:** dstruct_Interfaces.OSS.Inventory.equipmentsResponse
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/Interfaces/OSS/Inventory/iface_locations.xml

---

## Interfaces.Oss.Nid.Litont.Getlitontdetails

**Service:** LitOnt
**Operation:** getLitOntDetails
**Type:** Request-Response
**Request_Structure:** 
**Response_Structure:** dstruct_Interfaces.OSS.Nid.ontResponse
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/Interfaces/OSS/Nid/iface_LitOnt.xml

---

## Interfaces.Oss.Nid.Ont.Ontportsactivate

**Service:** Ont
**Operation:** ontPortsActivate
**Type:** Request-Response
**Request_Structure:** dstruct_Interfaces.OSS.Nid.activateOntPortsRequest
**Response_Structure:** dstruct_Interfaces.OSS.Nid.activateOntPortsResponse
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/Interfaces/OSS/Nid/iface_Ont.xml

---

## Interfaces.Oss.Nid.Ont.Getontbyserialnumber

**Service:** Ont
**Operation:** getONTBySerialNumber
**Type:** Request-Response
**Request_Structure:** 
**Response_Structure:** dstruct_Interfaces.OSS.Nid.ont
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/Interfaces/OSS/Nid/iface_Ont.xml

---

## Interfaces.Oss.Nid.Ont.Ontportsdeactivate

**Service:** Ont
**Operation:** ontPortsDeactivate
**Type:** Request-Response
**Request_Structure:** dstruct_Interfaces.OSS.Nid.activateOntPortsRequest
**Response_Structure:** dstruct_Interfaces.OSS.Nid.activateOntPortsResponse
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/Interfaces/OSS/Nid/iface_Ont.xml

---

## Interfaces.Oss.Rg.Residentialgateways.Getresidentialgateways

**Service:** residentialGateways
**Operation:** getResidentialgateways
**Type:** Request-Response
**Request_Structure:** 
**Response_Structure:** dstruct_Interfaces.OSS.RG.getResidentialgatewaysResponse
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/Interfaces/OSS/RG/iface_residentialGateways.xml

---

## Interfaces.Oss.Servicequalification.Servicequalification.Instantactivationstatus

**Service:** ServiceQualification
**Operation:** instantActivationStatus
**Type:** Request-Response
**Request_Structure:** 
**Response_Structure:** dstruct_Interfaces.OSS.ServiceQualification.InstantActivationStatusResponse
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/Interfaces/OSS/ServiceQualification/iface_ServiceQualification.xml

---

## Interfaces.Oss.Subscriberprov.Locations.Createlocations

**Service:** Locations
**Operation:** createLocations
**Type:** Request-Response
**Request_Structure:** dstruct_Interfaces.OSS.SubscriberProv.location
**Response_Structure:** dstruct_Interfaces.OSS.SubscriberProv.location
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/Interfaces/OSS/SubscriberProv/iface_Locations.xml

---

## Interfaces.Oss.Subscriberprov.Locations.Locationsexists

**Service:** Locations
**Operation:** locationsExists
**Type:** Request-Response
**Request_Structure:** 
**Response_Structure:** 
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/Interfaces/OSS/SubscriberProv/iface_Locations.xml

---

## Interfaces.Oss.Subscriberprov.Locations.Getlocationbyid

**Service:** Locations
**Operation:** getLocationById
**Type:** Request-Response
**Request_Structure:** 
**Response_Structure:** dstruct_Interfaces.OSS.SubscriberProv.location
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/Interfaces/OSS/SubscriberProv/iface_Locations.xml

---

## Interfaces.Oss.Subscriberprov.Subscribers.Createsubscriber

**Service:** Subscribers
**Operation:** createSubscriber
**Type:** Request-Response
**Request_Structure:** dstruct_Interfaces.OSS.SubscriberProv.subscriber
**Response_Structure:** dstruct_Interfaces.OSS.SubscriberProv.subscriber
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/Interfaces/OSS/SubscriberProv/iface_Subscribers.xml

---

## Interfaces.Oss.Subscriberprov.Subscribers.Updatesubscriberwithlocationid

**Service:** Subscribers
**Operation:** updateSubscriberWithLocationId
**Type:** Request-Response
**Request_Structure:** dstruct_Interfaces.OSS.SubscriberProv.subscriber
**Response_Structure:** dstruct_Interfaces.OSS.SubscriberProv.response
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/Interfaces/OSS/SubscriberProv/iface_Subscribers.xml

---

## Interfaces.Oss.Subscriberprov.Subscribers.Subscriberexists

**Service:** Subscribers
**Operation:** subscriberExists
**Type:** Request-Response
**Request_Structure:** 
**Response_Structure:** 
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/Interfaces/OSS/SubscriberProv/iface_Subscribers.xml

---

## Interfaces.Oss.Subscriberprov.Subscribers.Getsubscriberbyid

**Service:** Subscribers
**Operation:** getSubscriberById
**Type:** Request-Response
**Request_Structure:** 
**Response_Structure:** dstruct_Interfaces.OSS.SubscriberProv.subscriber
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/Interfaces/OSS/SubscriberProv/iface_Subscribers.xml

---

## Interfaces.Oss.Subscriberprov.Subscriptions.Getsubscription

**Service:** Subscriptions
**Operation:** getSubscription
**Type:** Request-Response
**Request_Structure:** 
**Response_Structure:** dstruct_Interfaces.OSS.SubscriberProv.subscriptionResponse
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/Interfaces/OSS/SubscriberProv/iface_Subscriptions.xml

---

## Interfaces.Oss.Subscriberprov.Subscriptions.Createsubscription

**Service:** Subscriptions
**Operation:** createSubscription
**Type:** Request-Response
**Request_Structure:** dstruct_Interfaces.OSS.SubscriberProv.subscriptionResponse
**Response_Structure:** dstruct_Interfaces.OSS.SubscriberProv.subscriptionResponse
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/Interfaces/OSS/SubscriberProv/iface_Subscriptions.xml

---

## Interfaces.Oss.Subscriberprov.Subscriptions.Deletesubscription

**Service:** Subscriptions
**Operation:** deleteSubscription
**Type:** Request-Response
**Request_Structure:** 
**Response_Structure:** dstruct_Interfaces.OSS.SubscriberProv.subscriptionsDS
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/Interfaces/OSS/SubscriberProv/iface_Subscriptions.xml

---

## Interfaces.Oss.Subscriberprov.Thirdpartyaccounts.Getthirdpartyaccount

**Service:** ThirdPartyAccounts
**Operation:** getThirdPartyAccount
**Type:** Request-Response
**Request_Structure:** 
**Response_Structure:** dstruct_Interfaces.OSS.SubscriberProv.thirdPartyAccount
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/Interfaces/OSS/SubscriberProv/iface_ThirdPartyAccounts.xml

---

## Interfaces.Oss.Subscriberprov.Thirdpartyaccounts.Createthirdpartyaccount

**Service:** ThirdPartyAccounts
**Operation:** createThirdPartyAccount
**Type:** Request-Response
**Request_Structure:** dstruct_Interfaces.OSS.SubscriberProv.thirdPartyAccount
**Response_Structure:** dstruct_Interfaces.OSS.SubscriberProv.thirdPartyAccount
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/Interfaces/OSS/SubscriberProv/iface_ThirdPartyAccounts.xml

---

## Interfaces.Oss.Subscriberprov.Thirdpartyaccounts.Deletethirdpartyaccount

**Service:** ThirdPartyAccounts
**Operation:** deleteThirdPartyAccount
**Type:** Request-Response
**Request_Structure:** 
**Response_Structure:** dstruct_Interfaces.OSS.SubscriberProv.thirdPartyAccount
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/Interfaces/OSS/SubscriberProv/iface_ThirdPartyAccounts.xml

---

## Interfaces.Oss.Subscriberprov.Thirdpartyaccounts.Updatethirdpartyaccount

**Service:** ThirdPartyAccounts
**Operation:** updateThirdPartyAccount
**Type:** Request-Response
**Request_Structure:** dstruct_Interfaces.OSS.SubscriberProv.thirdPartyAccount
**Response_Structure:** 
**Description:** 
**File_Path:** Trunk/FrontierOM/metadata/Interfaces/OSS/SubscriberProv/iface_ThirdPartyAccounts.xml

---
