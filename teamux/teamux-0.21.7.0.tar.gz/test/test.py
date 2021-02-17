from time import sleep

from teamux import tmux


def test_s_window_new():
    w = tmux.active.new('test_new')
    w.close()


def test_n_window_split():
    w = tmux.active.new('test_split')
    w.split()
    w.close()


def test_f_pane_resize():
    w = tmux.active.new('test_resize')
    w.split()
    w.right.width = 20
    sleep(2)
    w.left.width = 30
    sleep(2)
    w.left.width = 90
    w.close()


def test_f_pane_zoom():
    w = tmux.active.new('test_resize')
    w.split()
    w.right.send('# RIGHT')
    w.left.send('# LEFT')
    sleep(2)
    w.right.zoom()
    sleep(2)
    w.right.zoom()
    w.left.zoom()
    sleep(2)
    w.left.zoom()
    sleep(2)
    w.close()
