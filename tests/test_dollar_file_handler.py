import pytest
from unittest.mock import mock_open, patch

from cashregister.stream import filesystem
from cashregister.factory import creator


@pytest.mark.parametrize(
    [
        "data",
    ],
    [
        ("2.12,3.00\n1.97,2.00\n",),
        ("2.12,3.00\n1.97,2.00",),
    ],
)
def test_valid_file(data):
    dyn_handler = creator.create_dollar_denominator_with_random_case()

    mock_file = mock_open(read_data=data)

    with patch.object(filesystem, "open", mock_file):
        dyn_handler.run(input="input", output="output")

    output = [c.args[0] for c in mock_file.return_value.write.call_args_list]

    assert output == [
        "3 quarters,1 dime,3 pennies",
        "\n3 pennies",
    ]
    

@pytest.mark.parametrize(
    [
        "data",
    ],
    [
        ("2.12,3.00\n1.97,2.00\n1.0,2.0,3.0\n",),
        ("2.12,3.00\n1.97,2.00\n1.0\n",),
        ("2.12,3.00\n\n",),
        ("\n"),
    ],
)
def test_invalid_file_expected_two_attributes(data):
    dyn_handler = creator.create_dollar_denominator_with_random_case()

    mock_file = mock_open(read_data=data)

    with pytest.raises(ExceptionGroup), patch.object(filesystem, "open", mock_file):
        dyn_handler.run(input="input", output="output")



def test_invalid_file_expected_float():
    dyn_handler = creator.create_dollar_denominator_with_random_case()

    mock_file = mock_open(read_data="2.12,3.00\n1.97,a\n")

    with pytest.raises(ExceptionGroup), patch.object(filesystem, "open", mock_file):
        dyn_handler.run(input="input", output="output")
