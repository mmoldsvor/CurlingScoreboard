#include "sdk_common.h"
#include "ble_srv_common.h"
#include "ble_curl.h"
#include <string.h>
#include "nrf_gpio.h"
#include "boards.h"
#include "nrf_log.h"

static uint32_t capacative_value_char_add(ble_curls_t * p_curls, const ble_curls_init_t * p_curls_init)
{
    uint32_t            err_code;
    ble_gatts_char_md_t char_md;
    ble_gatts_attr_md_t cccd_md;
    ble_gatts_attr_t    attr_char_value;
    ble_uuid_t          ble_uuid;
    ble_gatts_attr_md_t attr_md;

    memset(&char_md, 0, sizeof(char_md));

    char_md.char_props.read   = 1;
    char_md.char_props.write  = 1;
    char_md.char_props.notify = 1;
    char_md.p_char_user_desc  = NULL;
    char_md.p_char_pf         = NULL;
    char_md.p_user_desc_md    = NULL;
    char_md.p_cccd_md         = &cccd_md;
    char_md.p_sccd_md         = NULL;

    memset(&attr_md, 0, sizeof(attr_md));

    attr_md.read_perm  = p_curls_init->capacative_value_char_attr_md.read_perm;
    attr_md.write_perm = p_curls_init->capacative_value_char_attr_md.write_perm;
    attr_md.vloc       = BLE_GATTS_VLOC_STACK;
    attr_md.rd_auth    = 0;
    attr_md.wr_auth    = 0;
    attr_md.vlen       = 0;

    ble_uuid.type = p_curls->uuid_type;
    ble_uuid.uuid = CAPACATIVE_CHAR_UUID;

    memset(&attr_char_value, 0, sizeof(attr_char_value));

    attr_char_value.p_uuid    = &ble_uuid;
    attr_char_value.p_attr_md = &attr_md;
    attr_char_value.init_len  = sizeof(bool);
    attr_char_value.init_offs = 0;
    attr_char_value.max_len   = sizeof(bool);

    memset(&cccd_md, 0, sizeof(cccd_md));

    //  Read  operation on Cccd should be possible without authentication.
    BLE_GAP_CONN_SEC_MODE_SET_OPEN(&cccd_md.read_perm);
    BLE_GAP_CONN_SEC_MODE_SET_OPEN(&cccd_md.write_perm);
    
    cccd_md.vloc              = BLE_GATTS_VLOC_STACK;

    err_code = sd_ble_gatts_characteristic_add(p_curls->service_handle, &char_md,
                                               &attr_char_value,
                                               &p_curls->capacative_value_handles);
    if (err_code != NRF_SUCCESS)
    {
        return err_code;
    }

    return NRF_SUCCESS;
}

static uint32_t movement_value_char_add(ble_curls_t * p_curls, const ble_curls_init_t * p_curls_init)
{
    uint32_t            err_code;
    ble_gatts_char_md_t char_md;
    ble_gatts_attr_md_t cccd_md;
    ble_gatts_attr_t    attr_char_value;
    ble_uuid_t          ble_uuid;
    ble_gatts_attr_md_t attr_md;

    memset(&char_md, 0, sizeof(char_md));

    char_md.char_props.read   = 1;
    char_md.char_props.write  = 1;
    char_md.char_props.notify = 1;
    char_md.p_char_user_desc  = NULL;
    char_md.p_char_pf         = NULL;
    char_md.p_user_desc_md    = NULL;
    char_md.p_cccd_md         = &cccd_md;
    char_md.p_sccd_md         = NULL;

    memset(&attr_md, 0, sizeof(attr_md));

    attr_md.read_perm  = p_curls_init->movement_value_char_attr_md.read_perm;
    attr_md.write_perm = p_curls_init->movement_value_char_attr_md.write_perm;
    attr_md.vloc       = BLE_GATTS_VLOC_STACK;
    attr_md.rd_auth    = 0;
    attr_md.wr_auth    = 0;
    attr_md.vlen       = 0;

    ble_uuid.type = p_curls->uuid_type;
    ble_uuid.uuid = MOVEMENT_CHAR_UUID;

    memset(&attr_char_value, 0, sizeof(attr_char_value));

    attr_char_value.p_uuid    = &ble_uuid;
    attr_char_value.p_attr_md = &attr_md;
    attr_char_value.init_len  = sizeof(bool);
    attr_char_value.init_offs = 0;
    attr_char_value.max_len   = sizeof(bool);

    memset(&cccd_md, 0, sizeof(cccd_md));

    //  Read  operation on Cccd should be possible without authentication.
    BLE_GAP_CONN_SEC_MODE_SET_OPEN(&cccd_md.read_perm);
    BLE_GAP_CONN_SEC_MODE_SET_OPEN(&cccd_md.write_perm);
    
    cccd_md.vloc              = BLE_GATTS_VLOC_STACK;

    err_code = sd_ble_gatts_characteristic_add(p_curls->service_handle, &char_md,
                                               &attr_char_value,
                                               &p_curls->movement_value_handles);
    if (err_code != NRF_SUCCESS)
    {
        return err_code;
    }

    return NRF_SUCCESS;
}

static uint32_t identifier_value_char_add(ble_curls_t * p_curls, const ble_curls_init_t * p_curls_init)
{
    uint32_t            err_code;
    ble_gatts_char_md_t char_md;
    ble_gatts_attr_md_t cccd_md;
    ble_gatts_attr_t    attr_char_value;
    ble_uuid_t          ble_uuid;
    ble_gatts_attr_md_t attr_md;

    memset(&char_md, 0, sizeof(char_md));

    char_md.char_props.read   = 1;
    char_md.char_props.write  = 1;
    char_md.char_props.notify = 1;
    char_md.p_char_user_desc  = NULL;
    char_md.p_char_pf         = NULL;
    char_md.p_user_desc_md    = NULL;
    char_md.p_cccd_md         = &cccd_md;
    char_md.p_sccd_md         = NULL;

    memset(&attr_md, 0, sizeof(attr_md));

    attr_md.read_perm  = p_curls_init->identifier_value_char_attr_md.read_perm;
    attr_md.write_perm = p_curls_init->identifier_value_char_attr_md.write_perm;
    attr_md.vloc       = BLE_GATTS_VLOC_STACK;
    attr_md.rd_auth    = 0;
    attr_md.wr_auth    = 0;
    attr_md.vlen       = 0;

    ble_uuid.type = p_curls->uuid_type;
    ble_uuid.uuid = IDENTIFIER_CHAR_UUID;

    memset(&attr_char_value, 0, sizeof(attr_char_value));

    attr_char_value.p_uuid    = &ble_uuid;
    attr_char_value.p_attr_md = &attr_md;
    attr_char_value.init_len  = sizeof(uint8_t);
    attr_char_value.init_offs = 0;
    attr_char_value.max_len   = sizeof(uint8_t);

    memset(&cccd_md, 0, sizeof(cccd_md));

    //  Read  operation on Cccd should be possible without authentication.
    BLE_GAP_CONN_SEC_MODE_SET_OPEN(&cccd_md.read_perm);
    BLE_GAP_CONN_SEC_MODE_SET_OPEN(&cccd_md.write_perm);
    
    cccd_md.vloc              = BLE_GATTS_VLOC_STACK;

    err_code = sd_ble_gatts_characteristic_add(p_curls->service_handle, &char_md,
                                               &attr_char_value,
                                               &p_curls->identifier_value_handles);
    if (err_code != NRF_SUCCESS)
    {
        return err_code;
    }

    return NRF_SUCCESS;
}

static void on_connect(ble_curls_t * p_curls, ble_evt_t const * p_ble_evt)
{
    p_curls->conn_handle = p_ble_evt->evt.gap_evt.conn_handle;

    ble_curls_evt_t evt;

    evt.evt_type = BLE_CURLS_EVT_CONNECTED;

    p_curls->evt_handler(p_curls, &evt);
}

static void on_disconnect(ble_curls_t * p_curls, ble_evt_t const * p_ble_evt)
{
    UNUSED_PARAMETER(p_ble_evt);

    p_curls->conn_handle = BLE_CONN_HANDLE_INVALID;
}

static void on_write(ble_curls_t * p_curls, ble_evt_t const * p_ble_evt)
{
    ble_gatts_evt_write_t * p_evt_write = &p_ble_evt->evt.gatts_evt.params.write;

    if (p_evt_write->handle == p_curls->identifier_value_handles.value_handle)
    {
        ble_curls_evt_t evt;
        evt.evt_type = BLE_CURLS_EVT_IDENTIFIER_UPDATED;
        evt.identifier_value = *p_evt_write->data;
            
        p_curls->evt_handler(p_curls, &evt);
    }

    if (((p_evt_write->handle == p_curls->capacative_value_handles.cccd_handle) || 
         (p_evt_write->handle == p_curls->movement_value_handles.cccd_handle))  && 
         (p_evt_write->len == 2))
    {

        // CCCD written, call application event handler
        if (p_curls->evt_handler != NULL)
        {
            ble_curls_evt_t evt;
            
            if (ble_srv_is_notification_enabled(p_evt_write->data))
            {
                evt.evt_type = BLE_CURLS_EVT_NOTIFICATION_ENABLED;
            }
            else
            {
                evt.evt_type = BLE_CURLS_EVT_NOTIFICATION_DISABLED;
            }
            // Call the application event handler.
            p_curls->evt_handler(p_curls, &evt);
        }
    }

    if ((p_evt_write->handle == p_curls->identifier_value_handles.cccd_handle) && (p_evt_write->len == 2))
    {
        // CCCD written, call application event handler
        if (p_curls->evt_handler != NULL)
        {
            ble_curls_evt_t evt;
            
            if (ble_srv_is_notification_enabled(p_evt_write->data))
            {
                evt.evt_type = BLE_CURLS_EVT_NOTIFICATION_IDENTIFIER_ENABLED;
            }
            // Call the application event handler.
            p_curls->evt_handler(p_curls, &evt);
        }
    }
}

uint32_t ble_curls_capacative_value_update(ble_curls_t * p_curls, bool capacative_value){
    if (p_curls == NULL)
    {
        return NRF_ERROR_NULL;
    }
    
    uint32_t err_code = NRF_SUCCESS;
    ble_gatts_value_t gatts_value;

    // Initialize value struct.
    memset(&gatts_value, 0, sizeof(gatts_value));

    gatts_value.len     = sizeof(bool);
    gatts_value.offset  = 0;
    gatts_value.p_value = &capacative_value;

    // Update database.
    err_code = sd_ble_gatts_value_set(p_curls->conn_handle,
                                        p_curls->capacative_value_handles.value_handle,
                                        &gatts_value);
    if (err_code != NRF_SUCCESS)
    {
        return err_code;
    }

    // Send value if connected and notifying.
    if ((p_curls->conn_handle != BLE_CONN_HANDLE_INVALID)) 
    {
        ble_gatts_hvx_params_t hvx_params;

        memset(&hvx_params, 0, sizeof(hvx_params));

        hvx_params.handle = p_curls->capacative_value_handles.value_handle;
        hvx_params.type   = BLE_GATT_HVX_NOTIFICATION;
        hvx_params.offset = gatts_value.offset;
        hvx_params.p_len  = &gatts_value.len;
        hvx_params.p_data = gatts_value.p_value;

        err_code = sd_ble_gatts_hvx(p_curls->conn_handle, &hvx_params);
    }
    else
    {
        err_code = NRF_ERROR_INVALID_STATE;
    }

    return err_code;
}

uint32_t ble_curls_movement_value_update(ble_curls_t * p_curls, bool movement_value){
    if (p_curls == NULL)
    {
        return NRF_ERROR_NULL;
    }
    
    uint32_t err_code = NRF_SUCCESS;
    ble_gatts_value_t gatts_value;

    // Initialize value struct.
    memset(&gatts_value, 0, sizeof(gatts_value));

    gatts_value.len     = sizeof(bool);
    gatts_value.offset  = 0;
    gatts_value.p_value = &movement_value;

    // Update database.
    err_code = sd_ble_gatts_value_set(p_curls->conn_handle,
                                        p_curls->movement_value_handles.value_handle,
                                        &gatts_value);
    if (err_code != NRF_SUCCESS)
    {
        return err_code;
    }

    // Send value if connected and notifying.
    if ((p_curls->conn_handle != BLE_CONN_HANDLE_INVALID)) 
    {
        ble_gatts_hvx_params_t hvx_params;

        memset(&hvx_params, 0, sizeof(hvx_params));

        hvx_params.handle = p_curls->movement_value_handles.value_handle;
        hvx_params.type   = BLE_GATT_HVX_NOTIFICATION;
        hvx_params.offset = gatts_value.offset;
        hvx_params.p_len  = &gatts_value.len;
        hvx_params.p_data = gatts_value.p_value;

        err_code = sd_ble_gatts_hvx(p_curls->conn_handle, &hvx_params);
    }
    else
    {
        err_code = NRF_ERROR_INVALID_STATE;
    }

    return err_code;
}

uint32_t ble_curls_identifier_value_update(ble_curls_t * p_curls, uint8_t identifier_value){
    if (p_curls == NULL)
    {
        return NRF_ERROR_NULL;
    }
    
    uint32_t err_code = NRF_SUCCESS;
    ble_gatts_value_t gatts_value;

    // Initialize value struct.
    memset(&gatts_value, 0, sizeof(gatts_value));

    gatts_value.len     = sizeof(uint8_t);
    gatts_value.offset  = 0;
    gatts_value.p_value = &identifier_value;

    // Update database.
    err_code = sd_ble_gatts_value_set(p_curls->conn_handle,
                                        p_curls->identifier_value_handles.value_handle,
                                        &gatts_value);
    
    // Send value if connected and notifying.
    if ((p_curls->conn_handle != BLE_CONN_HANDLE_INVALID)) 
    {
        ble_gatts_hvx_params_t hvx_params;

        memset(&hvx_params, 0, sizeof(hvx_params));

        hvx_params.handle = p_curls->identifier_value_handles.value_handle;
        hvx_params.type   = BLE_GATT_HVX_NOTIFICATION;
        hvx_params.offset = gatts_value.offset;
        hvx_params.p_len  = &gatts_value.len;
        hvx_params.p_data = gatts_value.p_value;

        err_code = sd_ble_gatts_hvx(p_curls->conn_handle, &hvx_params);
    }
    else
    {
        err_code = NRF_ERROR_INVALID_STATE;
    }

    return err_code;
}

void ble_curls_on_ble_evt( ble_evt_t const * p_ble_evt, void * p_context)
{
    ble_curls_t * p_curls = (ble_curls_t *) p_context;
    
    if (p_curls == NULL || p_ble_evt == NULL)
    {
        return;
    }

    switch (p_ble_evt->header.evt_id)
    {
        case BLE_GAP_EVT_CONNECTED:
            on_connect(p_curls, p_ble_evt);
            break;

        case BLE_GAP_EVT_DISCONNECTED:
            on_disconnect(p_curls, p_ble_evt);
            break;

        case BLE_GATTS_EVT_WRITE:
            on_write(p_curls, p_ble_evt);
            break;

        default:
            // No implementation needed.
            break;
    }
}

uint32_t ble_curls_init(ble_curls_t * p_curls, const ble_curls_init_t * p_curls_init)
{
    if (p_curls == NULL || p_curls_init == NULL)
    {
        return NRF_ERROR_NULL;
    }

    uint32_t   err_code;
    ble_uuid_t ble_uuid;

    p_curls->evt_handler   = p_curls_init->evt_handler;
    p_curls->conn_handle = BLE_CONN_HANDLE_INVALID;

    ble_uuid128_t base_uuid = {CURL_SERVICE_UUID_BASE};
    err_code =  sd_ble_uuid_vs_add(&base_uuid, &p_curls->uuid_type);
    VERIFY_SUCCESS(err_code);

    ble_uuid.type = p_curls->uuid_type;
    ble_uuid.uuid = CURL_SERVICE_UUID;

    err_code = sd_ble_gatts_service_add(BLE_GATTS_SRVC_TYPE_PRIMARY, &ble_uuid, &p_curls->service_handle);
    if (err_code != NRF_SUCCESS)
    {
        return err_code;
    }

    capacative_value_char_add(p_curls, p_curls_init);
    movement_value_char_add(p_curls, p_curls_init);
    identifier_value_char_add(p_curls, p_curls_init);

    return 0;
}