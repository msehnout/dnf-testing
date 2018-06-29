FILE(GLOB dnssec *.py)
INSTALL (FILES ${dnssec} DESTINATION ${PYTHON_INSTALL_DIR}/dnf/dnssec)
