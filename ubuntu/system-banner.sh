#!/usr/bin/env bash
# Fastfetch/neofetch-style banner for interactive Bash login shells.
[[ $- == *i* ]] || return 0
[[ -n "${UBUNTU_BANNER_SHOWN:-}" ]] && return 0
export UBUNTU_BANNER_SHOWN=1

C_ORANGE=$'\033[1;33m'; C_RED=$'\033[1;31m'; C_GREEN=$'\033[1;32m'; C_RESET=$'\033[0m'
. /etc/os-release 2>/dev/null || true
OS_NAME="${PRETTY_NAME:-Ubuntu}"
ARCH="$(uname -m 2>/dev/null || echo unknown)"
KERNEL="$(uname -r 2>/dev/null || echo unknown)"
UPTIME="$(uptime -p 2>/dev/null | sed 's/^up //' || echo unknown)"
CPU_COUNT="$(nproc 2>/dev/null || echo unknown)"
MEM_TOTAL="$(awk '/MemTotal/ {printf "%.1f GiB", $2/1048576}' /proc/meminfo 2>/dev/null)"
MEM_AVAIL="$(awk '/MemAvailable/ {printf "%.1f GiB", $2/1048576}' /proc/meminfo 2>/dev/null)"
DISK_INFO="$(df -h /data 2>/dev/null | awk 'NR==2 {printf "%s used / %s (%s)", $3, $2, $5}')"
TZ_NAME="${TZ:-$(cat /etc/timezone 2>/dev/null || echo UTC)}"
HOST_NAME="$(hostname 2>/dev/null || echo railway-container)"
BASH_LABEL="Bash ${BASH_VERSION:-unknown}"

if command -v fastfetch >/dev/null 2>&1; then
  fastfetch
else
  printf '\n%s        .-/+oossssoo+/-..            %s%s%s\n' "$C_ORANGE" "$C_GREEN" "${USER:-root}@${HOST_NAME}" "$C_RESET"
  printf '%s    `:+ssssssssssssssssss+:`        %sOS:%s       %s\n' "$C_ORANGE" "$C_RED" "$C_RESET" "$OS_NAME"
  printf '%s  -+ssssssssssssssssssyyssss+-      %sHost:%s     Railway Container\n' "$C_ORANGE" "$C_RED" "$C_RESET"
  printf '%s .ossssssssssssssssssdMMMNysssso.   %sKernel:%s   %s\n' "$C_ORANGE" "$C_RED" "$C_RESET" "$KERNEL"
  printf '%s /ssssssssssshdmmNNmmyNMMMMhssssss/  %sArch:%s     %s\n' "$C_ORANGE" "$C_RED" "$C_RESET" "$ARCH"
  printf '%s+ssssssssshmydMMMMMMMNddddyssssssss+ %sUptime:%s   %s\n' "$C_ORANGE" "$C_RED" "$C_RESET" "${UPTIME:-unknown}"
  printf '%s/sssssssshNMMMyhhyyyyhmNMMMNhsssssss/ %sShell:%s    %s\n' "$C_ORANGE" "$C_RED" "$C_RESET" "$BASH_LABEL"
  printf '%s.ssssssssdMMMNhsssssssssshNMMMdsssssss.%sCPU:%s      %s vCPU(s) detected\n' "$C_ORANGE" "$C_RED" "$C_RESET" "$CPU_COUNT"
  printf '%s +sssshhhyNMMNyssssssssssssyNMMMyssss+ %sMemory:%s   %s available / %s total\n' "$C_ORANGE" "$C_RED" "$C_RESET" "${MEM_AVAIL:-unknown}" "${MEM_TOTAL:-unknown}"
  printf '%s  ossyNMMMNyMMhsssssssssssssshmmmhssss/ %sDisk:%s     %s\n' "$C_ORANGE" "$C_RED" "$C_RESET" "${DISK_INFO:-unknown}"
  printf '%s   +ssssssssssshNMMMyssssssssssss+   %sTimezone:%s %s\n' "$C_ORANGE" "$C_RED" "$C_RESET" "$TZ_NAME"
  printf '%s    `:+ssssssssssssssssss+:`         %sDistro:%s   Ubuntu + Hermes Agent\n' "$C_ORANGE" "$C_RED" "$C_RESET"
fi

if pgrep -af '[h]ermes gateway run' >/dev/null 2>&1; then
  printf '%sHermes Gateway:%s %srunning%s\n\n' "$C_RED" "$C_RESET" "$C_GREEN" "$C_RESET"
else
  printf '%sHermes Gateway:%s %snot running / setup needed%s\n\n' "$C_RED" "$C_RESET" "$C_ORANGE" "$C_RESET"
fi
