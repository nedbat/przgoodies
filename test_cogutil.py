from cogutil import include_file, run_command

def test_file():
    me = __file__.rstrip("c")
    with open(me) as f:
        expected = f.readlines()
    assert include_file(me).lines == expected


def test_cmd():
    tp = run_command("seq 3")
    assert tp.lines == ["$ seq 3\n", "1\n", "2\n", "3\n"]


def test_bad_cmd():
    tp = run_command("exit 17")
    assert tp.lines == ["$ exit 17\n", "(exit code: 17)\n"]
