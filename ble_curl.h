#include <stdint.h>
#include <stdbool.h>
#include "ble.h"
#include "ble_srv_common.h"

#define CURL_SERVICE_UUID_BASE         {0xdd, 0xe3, 0x76, 0xb2, 0xf5, 0xe3, 0xc3, 0xac, \
                                          0x9a, 0x44, 0x23, 0xc2, 0x7b, 0x61, 0x60, 0x72}

#define CURL_SERVICE_UUID               0x0000
#define CAPACATIVE_CHAR_UUID            0x0001
#define MOVEMENT_CHAR_UUID              0x0002
#define IDENTIFIER_CHAR_UUID            0x0003

#define BLE_CURLS_DEF(_name)                                                                        \
static ble_curls_t _name;                                                                           \
NRF_SDH_BLE_OBSERVER(_name ## _obs,                                                                 \
                     BLE_HRS_BLE_OBSERVER_PRIO,                                                     \
                     ble_curls_on_ble_evt, &_name)

typedef enum
{
    BLE_CURLS_EVT_NOTIFICATION_ENABLED,
    BLE_CURLS_EVT_NOTIFICATION_DISABLED,
    BLE_CURLS_EVT_NOTIFICATION_IDENTIFIER_ENABLED,
    BLE_CURLS_EVT_DISCONNECTED,
    BLE_CURLS_EVT_CONNECTED,
    BLE_CURLS_EVT_IDENTIFIER_UPDATED
} ble_curls_evt_type_t;

typedef struct
{
    ble_curls_evt_type_t evt_type;
    uint8_t              identifier_value;
} ble_curls_evt_t;

typedef struct ble_curls_s ble_curls_t;
typedef void (*ble_curls_evt_handler_t) (ble_curls_t * p_curls, ble_curls_evt_t * p_evt);

typedef struct
{
    ble_curls_evt_handler_t       evt_handler;
    bool                          initial_capacative_value;
    ble_srv_cccd_security_mode_t  capacative_value_char_attr_md;
    bool                          initial_movement_value;
    ble_srv_cccd_security_mode_t  movement_value_char_attr_md;
    uint8_t                       initial_identifier_value;
    ble_srv_cccd_security_mode_t  identifier_value_char_attr_md;
} ble_curls_init_t;

struct ble_curls_s
{
    ble_curls_evt_handler_t       evt_handler;
    uint16_t                      service_handle;
    ble_gatts_char_handles_t      capacative_value_handles;
    ble_gatts_char_handles_t      movement_value_handles;
    ble_gatts_char_handles_t      identifier_value_handles;
    uint16_t                      conn_handle;
    uint8_t                       uuid_type; 
};


void ble_curls_on_ble_evt( ble_evt_t const * p_ble_evt, void * p_context);

uint32_t ble_curls_capacative_value_update(ble_curls_t * p_curls, bool capacative_value);

uint32_t ble_curls_movement_value_update(ble_curls_t * p_curls, bool movement_value);

uint32_t ble_curls_identifier_value_update(ble_curls_t * p_curls, uint8_t identifier_value);

uint32_t ble_curls_init(ble_curls_t * p_curls, const ble_curls_init_t * p_curls_init);