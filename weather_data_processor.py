import math
from datetime import date 
def calculate_dew_point(date_input = None, temp_min = None, temp_dew = None, TdewSubtract=2):
    if (isinstance(date_input, (date)) and isinstance(temp_min, (int, float)) and isinstance(temp_dew, (int, float)) and temp_dew <= temp_min):
        dew_point = temp_dew
    elif (isinstance(date_input, (date)) and isinstance(temp_min, (int, float))):
        dew_point = temp_min - TdewSubtract
    else:
        dew_point = None
    
    return dew_point

def calculate_saturration_vappour_pressure_at_temp(temp):
    if temp is None:
        return None
    else:
        return 0.6108 * math.exp( 17.27 * temp / (temp+237.3))

def calculate_solar_radiation_recorded(radiation=None, sunlight_hours=None, dailight_hours=None, temp_min=None, temp_max=None, extraterrestrial_solar_radiation=None):
    if isinstance(radiation, (int, float)):
        solar_radiation_recorded = radiation
    elif isinstance(sunlight_hours, (int, float)) and isinstance(dailight_hours, (int, float)):
        as_ = 0.25
        bs_ = 0.5
        solar_radiation_recorded = (as_ + bs_ * min(sunlight_hours/dailight_hours, 1)) * extraterrestrial_solar_radiation
    elif isinstance(temp_min, (int, float)) and isinstance(temp_max, (int, float)) and isinstance(extraterrestrial_solar_radiation, (int, float)):
        krs_ = 0.16
        solar_radiation_recorded = krs_ * math.sqrt(temp_max - temp_min) * extraterrestrial_solar_radiation
    else:
        solar_radiation_recorded = None

    return solar_radiation_recorded

def calculate_solar_radiation_clear_sky(extraterrestrial_solar_radiation):
    as_ = 0.25
    bs_ = 0.5
    solar_radiation_clear_sky = ( as_ + bs_ ) * extraterrestrial_solar_radiation
    
    return solar_radiation_clear_sky

def calculate_actual_vappour_pressure(temp_dry=None, temp_wet=None, temp_dew=None, rh_min=None, rh_max=None, rh_mean=None, saturration_vappour_pressure_at_temp_min=None, saturration_vappour_pressure_at_temp_max=None, saturration_vappour_pressure_at_temp_wet_bulb=None, saturration_vappour_pressure_at_temp_dew=None, atmospheric_pressure=None, apsy=0.000662):
    if isinstance(temp_dew, (int, float)):
        actual_vappour_pressure = saturration_vappour_pressure_at_temp_dew
    elif isinstance(saturration_vappour_pressure_at_temp_wet_bulb, (int, float)):
        actual_vappour_pressure = saturration_vappour_pressure_at_temp_wet_bulb - (apsy * atmospheric_pressure * (temp_dry - temp_wet))
    elif all(isinstance(i, (int, float)) for i in [rh_min, rh_max, saturration_vappour_pressure_at_temp_min, saturration_vappour_pressure_at_temp_max]):
        actual_vappour_pressure = ((saturration_vappour_pressure_at_temp_min * (rh_max) / 100) + (saturration_vappour_pressure_at_temp_max * rh_min / 100)) / 2
    elif all(isinstance(i, (int, float)) for i in [rh_max, saturration_vappour_pressure_at_temp_min]):
        actual_vappour_pressure = saturration_vappour_pressure_at_temp_min * rh_max / 100
    elif all(isinstance(i, (int, float)) for i in [rh_mean, saturration_vappour_pressure_at_temp_min, saturration_vappour_pressure_at_temp_max]):
        actual_vappour_pressure = (rh_mean / 100) * (saturration_vappour_pressure_at_temp_min + saturration_vappour_pressure_at_temp_max) / 2
    elif isinstance(saturration_vappour_pressure_at_temp_dew, (int, float)):
        actual_vappour_pressure = saturration_vappour_pressure_at_temp_dew
    else:
        actual_vappour_pressure = None

    return actual_vappour_pressure

def calculate_shortwave_radiation_net(solar_radiation_recorded, albedo=0.23):
    return ( 1 - albedo ) * solar_radiation_recorded

def calculate_longwave_radiation_net(temp_max, temp_min, actual_vappour_pressure, solar_radiation_recorded, solar_radiation_clear_sky):
    stefan_boltzmann = 4.903 * math.pow(10, -9)
    
    longwave_radiation_net = (stefan_boltzmann *
                             ((math.pow(temp_max+273.16, 4) + math.pow(temp_min+273.16, 4)) / 2) *
                             (0.34 - 0.14 * math.sqrt(actual_vappour_pressure)) *
                             ((1.35 * solar_radiation_recorded/solar_radiation_clear_sky) - 0.35)
                            )
    
    return longwave_radiation_net

def calculate_windspeed_at_2m_alt(anemometer_height, wind_speed, default_wind_speed=2):
    if all(isinstance(i, (int, float)) for i in [anemometer_height, wind_speed]):
        if anemometer_height == 2:
            result = max(wind_speed, 0.5)
        else:
            result = max((wind_speed * 4.87) / math.log(67.8 * anemometer_height - 5.42), 0.5)
    else:
        result = default_wind_speed
    return result