cmake_minimum_required(VERSION 3.28)

file(READ "${CMAKE_SOURCE_DIR}/CMakePresets.json" CONTENTS)
string(JSON LEN LENGTH "${CONTENTS}" workflowPresets)
math(EXPR STOP "${LEN} - 1")

if(NOT DEFINED FILTER)
    set(FILTER ".*")
endif()

foreach(i RANGE 0 ${STOP})
    string(JSON PRESET_NAME GET "${CONTENTS}" workflowPresets ${i} name)
    if(PRESET_NAME MATCHES "${FILTER}")
        execute_process(
            COMMAND ${CMAKE_COMMAND} --workflow --preset ${PRESET_NAME}
            RESULT_VARIABLE RET_CODE
        )
    endif()
endforeach()
