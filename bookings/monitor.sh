#!/bin/bash

LOG_PATH="../logs/api.log"
ENDPOINT="https://ghaymah.com/alert"
LAST_LINE_CHECKED_FILE="/tmp/monitor.lastline"

# Read last processed line number
last_line=$(cat "$LAST_LINE_CHECKED_FILE" 2>/dev/null || echo 0)
total_lines=$(wc -l < "$LOG_PATH")

if ! (command -v jq >/dev/null 2>&1); then
    sudo apt-get install -y jq
fi

#System info

function get_HOSTNAME(){
    echo "$(hostname)"
}
function get_IP(){
    echo "$(hostname -I | awk '{print $1}')"
}
function get_CPU_Usage(){
    echo "$(top -bn1 | grep "Cpu(s)" | awk '{print 100 - $8"%"}')"
}

function get_MEM_Usage(){
    echo "$(free -m | awk '/Mem/{printf "%.2f%%", $3/$2 * 100}')"
}

function get_DISK_Usage(){
    echo "$(df -h / | awk 'NR==2 {print $5}')"
}


function build_JSON() {
    local line="$1"  # log message as parameter

    local status_code
    status_code=$(echo "$line" | grep -oP 'status=\K[0-9]+')

    local timestamp
    timestamp=$(echo "$line" | grep -oP '^\[\K[^\]]+')

    JSON=$(jq -n \
        --arg host "$(get_HOSTNAME)" \
        --arg ip "$(get_IP)" \
        --arg cpu "$(get_CPU_Usage)" \
        --arg mem "$(get_MEM_Usage)" \
        --arg disk "$(get_DISK_Usage)" \
        --arg log "$line" \
        --arg error "$status_code" \
        --arg timestamp "$timestamp" \
        '{
            error: $error,
            timestamp: $timestamp,
            message: $log,
            server_metrics: {
                host: $host,
                ip: $ip,
                cpu: $cpu,
                mem: $mem,
                disk: $disk
            }
        }'
    )

    echo "$JSON"
}



# Process only new lines (used tail to display last new lines)
tail -n +"$((last_line+1))" "$LOG_PATH" | while read -r line; do
    line=$(echo "$line" | tr -d '\r')

    if echo "$line" | grep -E -q '(status=[45][0-9]{2}|failed|timeout)'; then
        #echo " Error detected: $line"

        build_JSON "$line"
        

        
        # Send alert
        #curl -X POST -H "Content-Type: application/json" -d "$JSON" "$ENDPOINT"
    fi
done

# Update last processed line
echo "$total_lines" > "$LAST_LINE_CHECKED_FILE"
