import pandas as pd

inputData = pd.read_csv('static/input.csv', index_col='variable').transpose()


class InputValues:
    social_security_amount = float(inputData['social_security_amount'])
    inflation = float(inputData['inflation'])
    inflation_variance = float(inputData['inflation_variance'])
    social_security_age = int(inputData['social_security_age'])
    retirement_phase_1_age = int(inputData['retirement_phase_1_age'])
    retirement_phase_2_age = int(inputData['retirement_phase_2_age'])
