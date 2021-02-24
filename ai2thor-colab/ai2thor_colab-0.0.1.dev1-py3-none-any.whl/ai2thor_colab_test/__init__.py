from IPython.display import HTML, display
import os


def start_server():
    def progress(value):
        return HTML(
            f"""
            <progress value='{value}' max="100", style='width: 100%'>
                {value}
            </progress>
        """
        )

    progress_bar = display(progress(0), display_id=True)

    try:
        import google.colab

        IN_COLAB = True
    except ImportError:
        IN_COLAB = False

    if IN_COLAB:
        with open("frame-buffer", "w") as writefile:
            writefile.write(
                """#taken from https://gist.github.com/jterrace/2911875
        XVFB=/usr/bin/Xvfb
        XVFBARGS=":1 -screen 0 1024x768x24 -ac +extension GLX +render -noreset"
        PIDFILE=./frame-buffer.pid
        case "$1" in
        start)
            /sbin/start-stop-daemon --start --quiet --pidfile $PIDFILE --make-pidfile --background --exec $XVFB -- $XVFBARGS
            ;;
        stop)
            /sbin/start-stop-daemon --stop --quiet --pidfile $PIDFILE
            rm $PIDFILE
            ;;
        restart)
            $0 stop
            $0 start
            ;;
        *)
                exit 1
        esac
        exit 0
            """
            )

        progress_bar.update(progress(5))
        os.system("apt-get install daemon >/dev/null 2>&1")

        progress_bar.update(progress(10))
        os.system("apt-get install wget >/dev/null 2>&1")

        progress_bar.update(progress(20))
        os.system(
            "wget http://security.ubuntu.com/ubuntu/pool/main/libx/libxfont/libxfont1_1.5.1-1ubuntu0.16.04.4_amd64.deb >/dev/null 2>&1"
        )

        progress_bar.update(progress(30))
        os.system(
            "wget --output-document xvfb.deb http://security.ubuntu.com/ubuntu/pool/universe/x/xorg-server/xvfb_1.18.4-0ubuntu0.11_amd64.deb >/dev/null 2>&1"
        )

        progress_bar.update(progress(40))
        os.system("dpkg -i libxfont1_1.5.1-1ubuntu0.16.04.4_amd64.deb >/dev/null 2>&1")

        progress_bar.update(progress(50))
        os.system("dpkg -i xvfb.deb >/dev/null 2>&1")

        progress_bar.update(progress(70))
        os.system("rm libxfont1_1.5.1-1ubuntu0.16.04.4_amd64.deb")

        progress_bar.update(progress(80))
        os.system("rm xvfb.deb")

        progress_bar.update(progress(90))
        os.system("bash frame-buffer start")

        os.environ["DISPLAY"] = ":1"
        progress_bar.update(progress(100))
