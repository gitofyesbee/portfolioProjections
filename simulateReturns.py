import pandas as pd
import numpy as np
from settings import InputValues
import locale

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')


# simulate returns
def simulate_returns(input_iterations, input_present_value, input_expected_roi, input_std_of_returns, input_current_age,
                     input_retirement_age,
                     input_annual_savings_till_retirement, input_annual_withdrawal_in_retirement, input_max_age):
    ending_values_df = pd.DataFrame()
    ending_percentile_df = pd.DataFrame()
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

    # get only 10%, 25%, 50%, 75% and 90% values
    percentile_list = [0.10, 0.25, 0.5, 0.75, 0.9]
    ending_values_transposed_df = ending_values_df.transpose()
    for percentile in percentile_list:
        temp_percentile_values = []
        for year in range(len(ending_values_df)):
            temp_percentile_values.append(ending_values_transposed_df[year].quantile(percentile))
        ending_percentile_df[percentile] = temp_percentile_values

    # get the minimum positive percentile in the final year
    pass_percentile = 0
    pass_percentile_value = 0
    final_year_median_value = ending_values_transposed_df[(len(ending_values_df) - 1)].median()
    for i in range(100):
        percentile_to_check = i / 100
        pass_percentile_value = ending_values_transposed_df[(len(ending_values_df) - 1)].quantile(percentile_to_check)
        if pass_percentile_value > 0:
            pass_percentile = 1 - percentile_to_check
            break

    provide_improvement_suggestions = True
    # Plan verdict
    if 0.00 <= pass_percentile < 0.60:
        verdict = "Guaranteed to fail. Rehash plan."
    elif 0.60 <= pass_percentile < 0.70:
        verdict = "Risky, recheck parameters. Exercise caution."
    elif 0.70 <= pass_percentile < 0.80:
        verdict = "Your plan is okay. Continue monitoring."
    elif 0.80 <= pass_percentile < 0.85:
        verdict = "Good Job. Your plan has a very high probability of success"
    else:
        verdict = "Congratulations. Unless there is a global catastrophe, your plan will succeed."
        provide_improvement_suggestions = False

    # format the return values
    formatted_pass_percentile = "{0:.2%}".format(pass_percentile)
    formatted_pass_percentile_value = locale.currency(pass_percentile_value, grouping=True)
    formatted_final_year_median_value = locale.currency(final_year_median_value, grouping=True)

    # return
    return ending_percentile_df.transpose(), formatted_pass_percentile, formatted_pass_percentile_value, \
           formatted_final_year_median_value, verdict, provide_improvement_suggestions
