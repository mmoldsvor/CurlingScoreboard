#include "sdk_common.h"

#include "ble_curls_c.h"
#include "ble_db_discovery.h"
#include "ble_types.h"
#include "ble_gattc.h"
#define NRF_LOG_MODULE_NAME ble_curls_c
#include "nrf_log.h"

NRF_LOG_MODULE_REGISTER();

#define WRITE_MESSAGE_LENGTH   BLE_CCCD_VALUE_LEN

static void gatt_error_handler(uint32_t nrf_error, void * p_ctx, uint16_t   conn_handle)
{
    ble_curls_c_t * p_ble_curls_c = (ble_curls_c_t *)p_ctx;

    NRF_LOG_DEBUG("A GATT Client error has occurred on conn_handle: 0X%X", conn_handle);

    if (p_ble_curls_c->error_handler != NULL)
    {
        p_ble_curls_c->error_handler(nrf_error);
    }
}

static void on_hvx(ble_curls_c_t * p_ble_curls_c, ble_evt_t const * p_ble_evt)
{
    // Check if the event is on the link for this instance.
    if (p_ble_curls_c->conn_handle != p_ble_evt->evt.gattc_evt.conn_handle)
    {
        return;
    }
    // Check if this is a Button notification.
    if (p_ble_evt->evt.gattc_evt.params.hvx.handle == p_ble_curls_c->peer_curls_db.capacative_value_handle)
    {
        if (p_ble_evt->evt.gattc_evt.params.hvx.len == 1)
        {
            ble_curls_c_evt_t ble_curls_c_evt;

            ble_curls_c_evt.evt_type                   = BLE_CURLS_C_EVT_CAPACATIVE_NOTIFICATION;
            ble_curls_c_evt.conn_handle                = p_ble_curls_c->conn_handle;
            ble_curls_c_evt.params.capacative_value    = p_ble_evt->evt.gattc_evt.params.hvx.data[0];
            
            p_ble_curls_c->evt_handler(p_ble_curls_c, &ble_curls_c_evt);
        }
    }
    else if (p_ble_evt->evt.gattc_evt.params.hvx.handle == p_ble_curls_c->peer_curls_db.movement_value_handle)
    {
        if (p_ble_evt->evt.gattc_evt.params.hvx.len == 1)
        {
            ble_curls_c_evt_t ble_curls_c_evt;

            ble_curls_c_evt.evt_type                    = BLE_CURLS_C_EVT_MOVEMENT_NOTIFICATION;
            ble_curls_c_evt.conn_handle                 = p_ble_curls_c->conn_handle;
            ble_curls_c_evt.params.movement_value       = p_ble_evt->evt.gattc_evt.params.hvx.data[0];

            p_ble_curls_c->evt_handler(p_ble_curls_c, &ble_curls_c_evt);
        }
    }
    else if (p_ble_evt->evt.gattc_evt.params.hvx.handle == p_ble_curls_c->peer_curls_db.identifier_value_handle)
    {
        if (p_ble_evt->evt.gattc_evt.params.hvx.len == 1)
        {
            ble_curls_c_evt_t ble_curls_c_evt;

            ble_curls_c_evt.evt_type                    = BLE_CURLS_C_EVT_IDENTIFIER_NOTIFICATION;
            ble_curls_c_evt.conn_handle                 = p_ble_curls_c->conn_handle;
            ble_curls_c_evt.params.identifier_value     = p_ble_evt->evt.gattc_evt.params.hvx.data[0];

            p_ble_curls_c->evt_handler(p_ble_curls_c, &ble_curls_c_evt);
        }
    }
}

static void on_disconnected(ble_curls_c_t * p_ble_curls_c, ble_evt_t const * p_ble_evt)
{
    if (p_ble_curls_c->conn_handle == p_ble_evt->evt.gap_evt.conn_handle)
    {
        p_ble_curls_c->conn_handle                                = BLE_CONN_HANDLE_INVALID;
        p_ble_curls_c->peer_curls_db.capacative_value_cccd_handle = BLE_GATT_HANDLE_INVALID;
        p_ble_curls_c->peer_curls_db.capacative_value_handle      = BLE_GATT_HANDLE_INVALID;
        p_ble_curls_c->peer_curls_db.movement_value_cccd_handle   = BLE_GATT_HANDLE_INVALID;
        p_ble_curls_c->peer_curls_db.movement_value_handle        = BLE_GATT_HANDLE_INVALID;
        p_ble_curls_c->peer_curls_db.identifier_value_cccd_handle = BLE_GATT_HANDLE_INVALID;
        p_ble_curls_c->peer_curls_db.identifier_value_handle      = BLE_GATT_HANDLE_INVALID;
    }
}

void ble_curls_on_db_disc_evt(ble_curls_c_t * p_ble_curls_c, ble_db_discovery_evt_t const * p_evt)
{
    // Check if the LED Button Service was discovered.
    if (p_evt->evt_type == BLE_DB_DISCOVERY_COMPLETE &&
        p_evt->params.discovered_db.srv_uuid.uuid == CURL_SERVICE_UUID &&
        p_evt->params.discovered_db.srv_uuid.type == p_ble_curls_c->uuid_type)
    {
        ble_curls_c_evt_t evt;

        evt.evt_type    = BLE_CURLS_C_EVT_DISCOVERY_COMPLETE;
        evt.conn_handle = p_evt->conn_handle;

        for (uint32_t i = 0; i < p_evt->params.discovered_db.char_count; i++)
        {
            const ble_gatt_db_char_t * p_char = &(p_evt->params.discovered_db.charateristics[i]);
            switch (p_char->characteristic.uuid.uuid)
            {
                case CAPACATIVE_CHAR_UUID:
                    evt.params.peer_db.capacative_value_handle      = p_char->characteristic.handle_value;
                    evt.params.peer_db.capacative_value_cccd_handle = p_char->cccd_handle;
                    break;

                case MOVEMENT_CHAR_UUID:
                    evt.params.peer_db.movement_value_handle        = p_char->characteristic.handle_value;
                    evt.params.peer_db.movement_value_cccd_handle   = p_char->cccd_handle;
                    break;

                case IDENTIFIER_CHAR_UUID:
                    evt.params.peer_db.identifier_value_handle        = p_char->characteristic.handle_value;
                    evt.params.peer_db.identifier_value_cccd_handle   = p_char->cccd_handle;
                    break;

                default:
                    break;
            }
        }

        NRF_LOG_DEBUG("LED Button Service discovered at peer.");
        //If the instance was assigned prior to db_discovery, assign the db_handles
        if (p_ble_curls_c->conn_handle != BLE_CONN_HANDLE_INVALID)
        {
            if ((p_ble_curls_c->peer_curls_db.capacative_value_handle      == BLE_GATT_HANDLE_INVALID) &&
                (p_ble_curls_c->peer_curls_db.capacative_value_cccd_handle == BLE_GATT_HANDLE_INVALID) &&
                (p_ble_curls_c->peer_curls_db.movement_value_handle        == BLE_GATT_HANDLE_INVALID) &&
                (p_ble_curls_c->peer_curls_db.movement_value_cccd_handle   == BLE_GATT_HANDLE_INVALID) &&
                (p_ble_curls_c->peer_curls_db.identifier_value_handle      == BLE_GATT_HANDLE_INVALID) &&
                (p_ble_curls_c->peer_curls_db.identifier_value_cccd_handle == BLE_GATT_HANDLE_INVALID))
            {
                p_ble_curls_c->peer_curls_db = evt.params.peer_db;
            }
        }

        p_ble_curls_c->evt_handler(p_ble_curls_c, &evt);
    }
}

uint32_t ble_curls_c_init(ble_curls_c_t * p_ble_curls_c, ble_curls_c_init_t * p_ble_curls_c_init)
{
    uint32_t      err_code;
    ble_uuid_t    curls_uuid;
    ble_uuid128_t curls_base_uuid = {CURL_SERVICE_UUID_BASE};

    VERIFY_PARAM_NOT_NULL(p_ble_curls_c);
    VERIFY_PARAM_NOT_NULL(p_ble_curls_c_init);
    VERIFY_PARAM_NOT_NULL(p_ble_curls_c_init->evt_handler);
    VERIFY_PARAM_NOT_NULL(p_ble_curls_c_init->p_gatt_queue);

    p_ble_curls_c->peer_curls_db.capacative_value_handle      = BLE_GATT_HANDLE_INVALID;
    p_ble_curls_c->peer_curls_db.capacative_value_cccd_handle = BLE_GATT_HANDLE_INVALID;
    p_ble_curls_c->peer_curls_db.movement_value_handle        = BLE_GATT_HANDLE_INVALID;
    p_ble_curls_c->peer_curls_db.movement_value_cccd_handle   = BLE_GATT_HANDLE_INVALID;
    p_ble_curls_c->peer_curls_db.identifier_value_handle      = BLE_GATT_HANDLE_INVALID;
    p_ble_curls_c->peer_curls_db.identifier_value_cccd_handle = BLE_GATT_HANDLE_INVALID;
    p_ble_curls_c->conn_handle                                = BLE_CONN_HANDLE_INVALID;
    p_ble_curls_c->evt_handler                                = p_ble_curls_c_init->evt_handler;
    p_ble_curls_c->p_gatt_queue                               = p_ble_curls_c_init->p_gatt_queue;
    p_ble_curls_c->error_handler                              = p_ble_curls_c_init->error_handler;

    err_code = sd_ble_uuid_vs_add(&curls_base_uuid, &p_ble_curls_c->uuid_type);
    if (err_code != NRF_SUCCESS)
    {
        return err_code;
    }
    VERIFY_SUCCESS(err_code);

    curls_uuid.type = p_ble_curls_c->uuid_type;
    curls_uuid.uuid = CURL_SERVICE_UUID;

    return ble_db_discovery_evt_register(&curls_uuid);
}

void ble_curls_c_on_ble_evt(ble_evt_t const * p_ble_evt, void * p_context)
{
    if ((p_context == NULL) || (p_ble_evt == NULL))
    {
        return;
    }

    ble_curls_c_t * p_ble_curls_c = (ble_curls_c_t *)p_context;

    switch (p_ble_evt->header.evt_id)
    {
        case BLE_GATTC_EVT_HVX:
            on_hvx(p_ble_curls_c, p_ble_evt);
            break;

        case BLE_GAP_EVT_DISCONNECTED:
            on_disconnected(p_ble_curls_c, p_ble_evt);
            break;

        default:
            break;
    }
}

static uint32_t capacative_cccd_configure(ble_curls_c_t * p_ble_curls_c, bool enable)
{
    NRF_LOG_DEBUG("Configuring CCCD. CCCD Handle = %d, Connection Handle = %d",
                  p_ble_curls_c->peer_curls_db.capacative_value_cccd_handle,
                  p_ble_curls_c->conn_handle);

    nrf_ble_gq_req_t cccd_req;
    uint16_t         cccd_val = enable ? BLE_GATT_HVX_NOTIFICATION : 0;
    uint8_t          cccd[WRITE_MESSAGE_LENGTH];

    cccd[0] = LSB_16(cccd_val);
    cccd[1] = MSB_16(cccd_val);

    cccd_req.type                        = NRF_BLE_GQ_REQ_GATTC_WRITE;
    cccd_req.error_handler.cb            = gatt_error_handler;
    cccd_req.error_handler.p_ctx         = p_ble_curls_c;
    cccd_req.params.gattc_write.handle   = p_ble_curls_c->peer_curls_db.capacative_value_cccd_handle;
    cccd_req.params.gattc_write.len      = WRITE_MESSAGE_LENGTH;
    cccd_req.params.gattc_write.offset   = 0;
    cccd_req.params.gattc_write.p_value  = cccd;
    cccd_req.params.gattc_write.write_op = BLE_GATT_OP_WRITE_REQ;

    return nrf_ble_gq_item_add(p_ble_curls_c->p_gatt_queue, &cccd_req, p_ble_curls_c->conn_handle);
}

static uint32_t movement_cccd_configure(ble_curls_c_t * p_ble_curls_c, bool enable)
{
    NRF_LOG_DEBUG("Configuring CCCD. CCCD Handle = %d, Connection Handle = %d",
                  p_ble_curls_c->peer_curls_db.movement_value_cccd_handle,
                  p_ble_curls_c->conn_handle);

    nrf_ble_gq_req_t cccd_req;
    uint16_t         cccd_val = enable ? BLE_GATT_HVX_NOTIFICATION : 0;
    uint8_t          cccd[WRITE_MESSAGE_LENGTH];

    cccd[0] = LSB_16(cccd_val);
    cccd[1] = MSB_16(cccd_val);

    cccd_req.type                        = NRF_BLE_GQ_REQ_GATTC_WRITE;
    cccd_req.error_handler.cb            = gatt_error_handler;
    cccd_req.error_handler.p_ctx         = p_ble_curls_c;
    cccd_req.params.gattc_write.handle   = p_ble_curls_c->peer_curls_db.movement_value_cccd_handle;
    cccd_req.params.gattc_write.len      = WRITE_MESSAGE_LENGTH;
    cccd_req.params.gattc_write.offset   = 0;
    cccd_req.params.gattc_write.p_value  = cccd;
    cccd_req.params.gattc_write.write_op = BLE_GATT_OP_WRITE_REQ;

    return nrf_ble_gq_item_add(p_ble_curls_c->p_gatt_queue, &cccd_req, p_ble_curls_c->conn_handle);
}

static uint32_t identifier_cccd_configure(ble_curls_c_t * p_ble_curls_c, bool enable)
{
    NRF_LOG_DEBUG("Configuring CCCD. CCCD Handle = %d, Connection Handle = %d",
                  p_ble_curls_c->peer_curls_db.identifier_value_cccd_handle,
                  p_ble_curls_c->conn_handle);

    nrf_ble_gq_req_t cccd_req;
    uint16_t         cccd_val = enable ? BLE_GATT_HVX_NOTIFICATION : 0;
    uint8_t          cccd[WRITE_MESSAGE_LENGTH];

    cccd[0] = LSB_16(cccd_val);
    cccd[1] = MSB_16(cccd_val);

    cccd_req.type                        = NRF_BLE_GQ_REQ_GATTC_WRITE;
    cccd_req.error_handler.cb            = gatt_error_handler;
    cccd_req.error_handler.p_ctx         = p_ble_curls_c;
    cccd_req.params.gattc_write.handle   = p_ble_curls_c->peer_curls_db.identifier_value_cccd_handle;
    cccd_req.params.gattc_write.len      = WRITE_MESSAGE_LENGTH;
    cccd_req.params.gattc_write.offset   = 0;
    cccd_req.params.gattc_write.p_value  = cccd;
    cccd_req.params.gattc_write.write_op = BLE_GATT_OP_WRITE_REQ;

    return nrf_ble_gq_item_add(p_ble_curls_c->p_gatt_queue, &cccd_req, p_ble_curls_c->conn_handle);
}

uint32_t ble_curls_c_capacative_notif_enable(ble_curls_c_t * p_ble_curls_c)
{
    VERIFY_PARAM_NOT_NULL(p_ble_curls_c);

    if (p_ble_curls_c->conn_handle == BLE_CONN_HANDLE_INVALID)
    {
        return NRF_ERROR_INVALID_STATE;
    }

    return capacative_cccd_configure(p_ble_curls_c, true);
}

uint32_t ble_curls_c_movement_notif_enable(ble_curls_c_t * p_ble_curls_c)
{
    VERIFY_PARAM_NOT_NULL(p_ble_curls_c);

    if (p_ble_curls_c->conn_handle == BLE_CONN_HANDLE_INVALID)
    {
        return NRF_ERROR_INVALID_STATE;
    }

    return movement_cccd_configure(p_ble_curls_c, true);
}

uint32_t ble_curls_c_identifier_notif_enable(ble_curls_c_t * p_ble_curls_c)
{
    VERIFY_PARAM_NOT_NULL(p_ble_curls_c);

    if (p_ble_curls_c->conn_handle == BLE_CONN_HANDLE_INVALID)
    {
        return NRF_ERROR_INVALID_STATE;
    }

    return identifier_cccd_configure(p_ble_curls_c, true);
}

uint32_t ble_curls_c_handles_assign(ble_curls_c_t * p_ble_curls_c, uint16_t conn_handle, const curls_db_t * p_peer_handles)
{
    VERIFY_PARAM_NOT_NULL(p_ble_curls_c);

    p_ble_curls_c->conn_handle = conn_handle;
    if (p_peer_handles != NULL)
    {
        p_ble_curls_c->peer_curls_db = *p_peer_handles;
    }
    return nrf_ble_gq_conn_handle_register(p_ble_curls_c->p_gatt_queue, conn_handle);
}