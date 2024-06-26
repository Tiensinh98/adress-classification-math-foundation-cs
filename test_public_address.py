import pytest
import time
import json
import numpy as np

import classifier as clf


@pytest.fixture(autouse=True)
def solution():
    return clf.Solution()


@pytest.mark.parametrize('case_file_path', [
    'test_cases/public.json',
    'test_cases/confusing_number_hcm_cases.json',
    'test_cases/inconsistent_information.json',
    'test_cases/other_cases.json'
])
def test_full_address_cases(solution, case_file_path):
    test_cases = json.load(open(case_file_path, encoding='utf-8'))
    count = 0
    timer = []
    print('Reading test case: ', case_file_path, '\n')
    for test_case in test_cases:
        start = time.time()
        output = solution.process(test_case['text'])
        time_elapsed = time.time() - start
        timer.append(time_elapsed)
        expected_result = test_case['result']
        ok = (expected_result['province'] == output['province']
              and expected_result['district'] == output['district']
              and expected_result['ward'] == output['ward'] and time_elapsed < 0.05)
        if ok:
            count += 1
        else:
            print('Failed!')
            print('Input Address', test_case['text'])
            print('Expected result', test_case['result'])
            print('Actual', output)
            print('Time Elapsed', time_elapsed)

    print(f'Passed: {count} cases / {len(test_cases)}')
    print("max: ", np.max(timer))
    print("avarage: ", np.average(timer))
    assert np.max(timer) < 0.2, 'Max time exceeds the allowed amount of time.'
    assert np.average(timer) < 4. / 100, 'Average time exceeds the allowed amount of time.'
