#!/bin/bash
# ETH Trading Cron Setup Script
# Prints the openclaw commands to set up the trading cron jobs

echo "Run these openclaw commands to set up the trading cron:"
echo ""
echo "# Trading brain - every 15 minutes, 9am-11pm EST"
echo "openclaw cron add --name 'ETH Trading Brain' --schedule '*/15 9-23 * * *' --task 'Read /home/openclaw/.openclaw/workspace/projects/eth-engine/data/brain-prompt.md and output ONLY a JSON trading decision. Write the JSON to /home/openclaw/.openclaw/workspace/projects/eth-engine/data/decision.json. Then run: cd /home/openclaw/.openclaw/workspace/projects/eth-engine && python3 execute-decision.py' --model 'minimax/MiniMax-M2.5'"
echo ""
echo "# Data validation - every 30 minutes"  
echo "openclaw cron add --name 'Data Validator' --schedule '*/30 * * * *' --task 'Run: cd /home/openclaw/.openclaw/workspace/projects/eth-engine && python3 validate-data.py. If exit code is 2, alert the user about data issues.' --model 'minimax/MiniMax-M2.5'"
echo ""
echo "# Data collection - every 15 minutes (runs BEFORE trading brain)"
echo "# Add to system crontab:"
echo "*/15 9-23 * * * cd /home/openclaw/.openclaw/workspace/projects/eth-engine && python3 collect-trading-context.py >> data/collect.log 2>&1"
