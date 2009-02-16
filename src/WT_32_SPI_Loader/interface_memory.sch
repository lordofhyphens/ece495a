VERSION 6
BEGIN SCHEMATIC
    BEGIN ATTR DeviceFamilyName "spartan2"
        DELETE all:0
        EDITNAME all:0
        EDITTRAIT all:0
    END ATTR
    BEGIN NETLIST
        SIGNAL SPI_OUT
        SIGNAL SPI_CLK
        PORT Output SPI_OUT
        PORT Output SPI_CLK
    END NETLIST
    BEGIN SHEET 1 3520 2720
        BEGIN BRANCH SPI_OUT
            WIRE 2160 944 2544 944
        END BRANCH
        IOMARKER 2544 944 SPI_OUT R0 28
        IOMARKER 2544 1104 SPI_CLK R0 28
        BEGIN BRANCH SPI_CLK
            WIRE 2160 1104 2544 1104
        END BRANCH
    END SHEET
END SCHEMATIC