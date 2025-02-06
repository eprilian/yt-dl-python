#!/bin/bash

# Set the log file location
LOG_FILE="yt_dl.log"

# Function to start the download
start_program() {
    # Run your Python script in the background and save output to the log file
    nohup python3 yt-dl.py >> "$LOG_FILE" 2>&1 &
    echo "Program started. Output is being logged to $LOG_FILE"
}

# Function to stop the download
stop_program() {
    # Find the process ID (PID) of the running Python script and terminate it
    PID=$(pgrep -f yt-dl.py)
    if [ -z "$PID" ]; then
        echo "No running yt-dl.py process found."
    else
        kill $PID
        echo "Program stopped."
    fi
}

# Function to show the current log
show_log() {
    tail -f "$LOG_FILE"
}

# Display the menu options
show_menu() {
    echo "--------------------------"
    echo "YouTube Download Manager"
    echo "--------------------------"
    echo "1) Start Program"
    echo "2) Stop Program"
    echo "3) Show Log"
    echo "4) Exit"
    echo "--------------------------"
}

# Handle the user choice
handle_choice() {
    read -p "Choose an option: " choice
    case "$choice" in
        1)
            start_program
            ;;
        2)
            stop_program
            ;;
        3)
            show_log
            ;;
        4)
            echo "Exiting..."
            exit 0
            ;;
        *)
            echo "Invalid choice. Please try again."
            ;;
    esac
}

# Main loop to show the menu and handle user input
while true; do
    show_menu
    handle_choice
done
