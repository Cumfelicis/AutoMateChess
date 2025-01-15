from backend.config import config

hall_voltage_to_piece = {  # maps the voltage measured at the hall-effect sensors to the different pieces
    100: 'b',
    150: 'n',
    200: 'r',
    250: 'q',
    300: 'k',
    350: 'p',
    650: 'B',
    700: 'N',
    750: 'R',
    800: 'Q',
    850: 'K',
    900: 'P'
}


def get_piece(voltage) -> str:  # ads logic to the mapping based on the Hall_Voltage_Scope to detect pieces
    for voltage in range(voltage - config['HALL_VOLTAGE_SCOPE'], voltage + config['HALL_VOLTAGE_SCOPE'] + 1):
        try:
            return hall_voltage_to_piece[voltage]
        except KeyError:
            pass
    return 'n'
