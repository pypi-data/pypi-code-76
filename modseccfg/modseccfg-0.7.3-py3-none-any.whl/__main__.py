# api: python
# type: virtual
# priority: hidden
# title: module invocation
# description: python -m modseccfg
# version: 0.0
# category: cli
#
# Just a wrapper to allow starting module directly.
#

if __name__ == "__main__":
    from modseccfg.mainwindow import main
    main()
