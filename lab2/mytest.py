import sys


def test(res, expt):
    if res != expt:
        print('FAILED. Expected: ' + str(expt) + ' Actual: ' + str(res), file=sys.stderr)
    else:
        print('PASSED. Expected: ' + str(expt) + ' Actual: ' + str(res))
    return res == expt