#include <stdint.h>
#include <stdbool.h>
#include "ble.h"
#include "ble_db_discovery.h"
#include "ble_srv_common.h"
#include "nrf_ble_gq.h"
#include "nrf_sdh_ble.h"

#define BLE_CURLS_C_DEF(_name)                                                                      \
static ble_curls_c_t _name;                                                                         \
NRF_SDH_BLE_OBSERVER(_name ## _obs,                                                                 \
                     BLE_HRS_C_BLE_OBSERVER_PRIO,                                                   \
                     ble_curls_c_on_ble_evt, &_name)

#define BLE_CURLS_C_ARRAY_DEF(_name, _cnt)                                                          \
static ble_curls_c_t _name[_cnt];                                                                   \
NRF_SDH_BLE_OBSERVERS(_name ## _obs,                                                                \
                      BLE_HRS_C_BLE_OBSERVER_PRIO,                                                  \
                      ble_curls_c_on_ble_evt, &_name, _cnt)

                      
#define CURL_SERVICE_UUID_BASE         {0xdd, 0xe3, 0x76, 0xb2, 0xf5, 0xe3, 0xc3, 0xac, \
                                        0x9a, 0x44, 0x23, 0xc2, 0x7b, 0x61, 0x60, 0x72}

#define CURL_SERVICE_UUID               0x0000
#define CAPACATIVE_CHAR_UUID            0x0001
#define MOVEMENT_CHAR_UUID              0x0002

typedef enum
{
    BLE_CURLS_C_EVT_DISCOVERY_COMPLETE = 1,
    BLE_CURLS_C_EVT_CAPACATIVE_NOTIFICATION,
    BLE_CURLS_C_EVT_MOVEMENT_NOTIFICATION,
    BLE_CURLS_C_EVT_DISCONNECTED
} ble_curls_c_evt_type_t;

typedef struct
{
    uint16_t capacative_value_cccd_handle;
    uint16_t capacative_value_handle;
    uint16_t movement_value_cccd_handle;
    uint16_t movement_value_handle;
} curls_db_t;

typedef struct
{
    ble_curls_c_evt_type_t  evt_type;
    uint16_t                conn_handle;
    union
    {
        bool                capacative_value;
        bool                movement_value;
        curls_db_t          peer_db;
    } params;
} ble_curls_c_evt_t;

typedef struct ble_curls_c_s ble_curls_c_t;

typedef void (* ble_curls_c_evt_handler_t) (ble_curls_c_t * p_ble_curls_c, ble_curls_c_evt_t * p_evt);

struct ble_curls_c_s
{
    uint16_t                    conn_handle;
    curls_db_t                  peer_curls_db;
    ble_curls_c_evt_handler_t   evt_handler;
    ble_srv_error_handler_t     error_handler;
    uint8_t                     uuid_type;
    nrf_ble_gq_t              * p_gatt_queue;
};

typedef struct
{
    ble_curls_c_evt_handler_t   evt_handler;
    nrf_ble_gq_t              * p_gatt_queue;
    ble_srv_error_handler_t     error_handler;
} ble_curls_c_init_t;

uint32_t ble_curls_c_init(ble_curls_c_t * p_ble_curls_c, ble_curls_c_init_t * p_ble_curls_c_init);

void ble_curls_c_on_ble_evt(ble_evt_t const * p_ble_evt, void * p_context);

uint32_t ble_curls_c_capacative_notif_enable(ble_curls_c_t * p_ble_curls_c);

uint32_t ble_curls_c_movement_notif_enable(ble_curls_c_t * p_ble_curls_c);

void ble_curls_on_db_disc_evt(ble_curls_c_t * p_ble_curls_c, const ble_db_discovery_evt_t * p_evt);

uint32_t ble_curls_c_handles_assign(ble_curls_c_t * p_ble_curls_c, uint16_t conn_handle, const curls_db_t * p_peer_handles);
