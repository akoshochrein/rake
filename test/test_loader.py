from src.loader import _get_argument_parser


def test_args_parser_loads_file_from_shorthand():
    # GIVEN
    expected_filename = 'test/fixtures/diophantine_equations.txt'
    parser = _get_argument_parser()

    # WHEN
    args = parser.parse_args(['-f', expected_filename])

    # THEN
    assert expected_filename == args.filename.name

def test_args_parser_loads_file_from_full_name():
    # GIVEN
    expected_filename = 'test/fixtures/diophantine_equations.txt'
    parser = _get_argument_parser()

    # WHEN
    args = parser.parse_args(['--filename', expected_filename])

    # THEN
    assert expected_filename == args.filename.name

def test_args_parser_poistional_param_works():
    # GIVEN
    expected_text = 'This text is supposed to be parsed.'
    parser = _get_argument_parser()

    # WHEN
    args = parser.parse_args([expected_text])

    # THEN
    assert expected_text == args.text
