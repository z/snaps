FROM python:3.8
LABEL maintainer="z@xnz.me"

ENV PATH="${PATH}:/home/app/.local/bin"

RUN apt-get update && apt-get install --no-install-recommends -y \
    dbus-x11 \
    gir1.2-gtk-3.0 \
    gir1.2-notify \
    libgirepository1.0-dev \
    notification-daemon \
    python3-gi \
    python3-gi-cairo \
    xauth \
    xvfb

RUN printf "[D-BUS Service]\n\
Name=org.freedesktop.Notifications\n\
Exec=/usr/lib/notification-daemon/notification-daemon" > /usr/share/dbus-1/services/org.freedesktop.Notifications.service

RUN service dbus start

RUN useradd --create-home app

WORKDIR /home/app
USER app

COPY --chown=app:app CHANGELOG.md LICENSE Makefile README.md requirements.in requirements-dev.in setup.py ./
COPY --chown=app:app src src/
COPY --chown=app:app tests tests/

RUN pip3 install --upgrade pip \
    && make develop
