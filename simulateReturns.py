import pandas as pd
import numpy as np
from settings import InputValues


# simulate returns
def simulate_returns(input_iterations, input_present_value, input_expected_roi, input_std_of_returns, input_current_age,
                     input_retirement_age,
                     input_annual_savings_till_retirement, input_annual_withdrawal_in_retirement, input_max_age):
    ending_values_df = pd.DataFrame()
    iterations = int(input_iterations)

    for iteration in range(iterations):
        # get values
        pv = float(input_present_value)
        expected_roi = float(input_expected_roi)
        std = float(input_std_of_returns)
        retire_in = (int(input_retirement_age) - int(input_current_age))
        duration = (int(input_max_age) - int(input_current_age))
        pmt = float(input_annual_savings_till_retirement)
        current_age = int(input_current_age)
        retirement_phase_1_age = InputValues.retirement_phase_1_age
        retirement_phase_2_age = InputValues.retirement_phase_2_age
        social_security_age = InputValues.social_security_age
        social_security_amount = InputValues.social_security_amount
        retirement_phase_1_expenses = float(input_annual_withdrawal_in_retirement)
        retirement_phase_2_expenses = (retirement_phase_1_expenses - social_security_amount)
        retirement_final_phase_expenses = (retirement_phase_2_expenses - 18000.00)
        withdrawal = retirement_phase_1_expenses
        inflation = InputValues.inflation
        inflation_variance = InputValues.inflation_variance
        temp_end_values = []

        # calculate returns
        for year in range(duration):
            anticipated_roi = np.random.normal(expected_roi, std)
            anticipated_inflation = np.random.normal(inflation, inflation_variance)

            # set withdrawal amount based on retirement phase
            if (retirement_phase_1_age - current_age) < year < (retirement_phase_2_age - current_age):
                withdrawal = retirement_phase_2_expenses
            elif year >= (retirement_phase_2_age - current_age):
                withdrawal = retirement_final_phase_expenses

            # core logic
            if year >= retire_in:
                pv = pv - withdrawal
            fv = round((pv * (1 + anticipated_roi)), 2)
            if year < retire_in:
                fv = fv + pmt
            if year > (social_security_age - current_age):
                fv = fv + social_security_amount
            temp_end_values.append(fv)
            pv = fv

            # adjust for inflation
            withdrawal = withdrawal * (1 + anticipated_inflation)
            retirement_phase_1_expenses = retirement_phase_1_expenses * (1 + anticipated_inflation)
            retirement_phase_2_expenses = retirement_phase_2_expenses * (1 + anticipated_inflation)
            retirement_final_phase_expenses = retirement_final_phase_expenses * (1 + anticipated_inflation)
            social_security_amount = social_security_amount * (1 + anticipated_inflation)

        ending_values_df[iteration] = temp_end_values
        print(ending_values_df.head(100))

    return ending_values_df
