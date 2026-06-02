name: Telegram Group Scheduler

env:
  FORCE_JAVASCRIPT_ACTIONS_TO_NODE24: true

on:
  schedule:
    # 07:00 Istanbul = 04:00 UTC
    - cron: "0 4 * * *"

    # 20:00 Istanbul = 17:00 UTC
    - cron: "0 17 * * *"

    # 23:50 Istanbul = 20:50 UTC
    - cron: "50 20 * * *"

    # 00:00 Istanbul = 21:00 UTC
    - cron: "0 21 * * *"

  workflow_dispatch:
    inputs:
      action:
        description: "open, ad, goodnight, close"
        required: true
        default: "open"

jobs:
  run:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - run: pip install -r requirements.txt

      - name: Set Action
        run: |
          if [ "${{ github.event_name }}" = "workflow_dispatch" ]; then
            echo "ACTION=${{ github.event.inputs.action }}" >> $GITHUB_ENV
          elif [ "${{ github.event.schedule }}" = "0 4 * * *" ]; then
            echo "ACTION=open" >> $GITHUB_ENV
          elif [ "${{ github.event.schedule }}" = "0 17 * * *" ]; then
            echo "ACTION=ad" >> $GITHUB_ENV
          elif [ "${{ github.event.schedule }}" = "50 20 * * *" ]; then
            echo "ACTION=goodnight" >> $GITHUB_ENV
          elif [ "${{ github.event.schedule }}" = "0 21 * * *" ]; then
            echo "ACTION=close" >> $GITHUB_ENV
          fi

      - name: Run Bot
        env:
          BOT_TOKEN: ${{ secrets.BOT_TOKEN }}
          GROUP_ID: ${{ secrets.GROUP_ID }}
          ACTION: ${{ env.ACTION }}
        run: python telegram_control.py
