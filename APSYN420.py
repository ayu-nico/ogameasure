# coding:utf_8
import time
import datetime
import sys
import socket
from ..SCPI import scpi

class PMX18_2A(scpi.scpi_family):
    manufacturer = 'KIKUSUI'
    product_name = 'PMX18'
    classification = 'Power Supply'

    _scpi_enable = '*CLS *ESE *ESR? *IDN? *OPC *OPT? *RCL *RST *SAV *SRE *STB? *TRG? *TST? *WAI'
