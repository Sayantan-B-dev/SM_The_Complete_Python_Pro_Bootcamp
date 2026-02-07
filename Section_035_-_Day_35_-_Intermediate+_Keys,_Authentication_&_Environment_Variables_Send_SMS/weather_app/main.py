import os
from app.entrypoints.cli import main as main_cli
from app.entrypoints.gui import main as main_gui
from app.entrypoints.sms import main as main_sms

MODE = os.getenv("APP_MODE", "cli")

if MODE == "cli":
    main_cli()
elif MODE == "gui":
    main_gui()
elif MODE == "sms":
    main_sms()
