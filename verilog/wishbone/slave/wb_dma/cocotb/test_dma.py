# Simple tests for an adder module
import cocotb
from cocotb.result import TestFailure
from model.dma import DMA
from model.sim_host import NysaSim
import time

CLK_PERIOD = 4

@cocotb.test(skip = True)
def first_test(dut):
    """
    Description:
        Initial Test

    Test ID: 0

    Expected Results:
        Write to all registers
    """

    dut.test_id = 0
    nysa = NysaSim(dut)
    yield(nysa.reset())
    nysa.read_sdb()

    #nysa.pretty_print_sdb()
    #dma = DMA(nysa, nysa.find_device(DMA)[0])
    dma = DMA(nysa, nysa.find_device(DMA)[0])
    yield cocotb.external(dma.setup)()
    print "Try a read"
    yield cocotb.external(dma.get_channel_count)()

    dut.log.info("DMA Opened!")
    dut.log.info("Ready")



@cocotb.test(skip = True)
def test_setup_dma(dut):
    """
    Description:
        Setup a channel

    Test ID: 1

    Expected Results:
        Write to all registers
    """

    dut.test_id = 1
    nysa = NysaSim(dut)
    yield(nysa.reset())
    nysa.read_sdb()

    dma = DMA(nysa, nysa.find_device(DMA)[0])
    yield cocotb.external(dma.setup)()
    yield cocotb.external(dma.enable_dma)(True)
    #yield nysa.wait_clocks(10)

    SINK_ADDR = 2
    INST_ADDR = 7
    for i in range (0, dma.channel_count):
        #print "w"
        yield cocotb.external(dma.set_channel_sink_addr)(i, SINK_ADDR)
        r = yield cocotb.external(dma.get_channel_sink_addr)(i)
        if SINK_ADDR != r:
            raise cocotb.result.TestFailure("Channel [%d] Sink Addr should be [%d] but is [%d]" % (i, SINK_ADDR, r))

        yield cocotb.external(dma.set_channel_instruction_pointer)(i, INST_ADDR)
        r = yield cocotb.external(dma.get_channel_instruction_pointer)(i)
        if INST_ADDR != r:
            raise cocotb.result.TestFailure("Channel [%d] Insruction Addr should be [%d] but is [%d]" % (i, INST_ADDR, r))

        yield cocotb.external(dma.enable_source_address_increment)(i, True)
        r = yield cocotb.external(dma.is_source_address_increment)(i)
        if r != True:
            raise cocotb.result.TestFailure("Channel [%d] source Addr should be [%d] but is [%d]" % (i, INST_ADDR, r))

        yield cocotb.external(dma.enable_source_address_increment)(i, False)
        r = yield cocotb.external(dma.is_source_address_increment)(i)
        if r != False:
            raise cocotb.result.TestFailure("Channel [%d] source Addr should be [%d] but is [%d]" % (i, INST_ADDR, r))



        yield cocotb.external(dma.enable_channel)(i, True)
        r = yield cocotb.external(dma.is_channel_enable)(i)

        if r == False:
            raise cocotb.result.TestFailure("Channel [%d] DMA Enable should be true but it is not" % (i))


        yield cocotb.external(dma.enable_channel)(i, False)
        r = yield cocotb.external(dma.is_channel_enable)(i)
        if r:
            raise cocotb.result.TestFailure("Channel [%d] DMA Enable should be false but it is not" % (i))


        #Enable and Disable the source incrementing
        yield cocotb.external(dma.enable_source_address_increment)(i, True)
        r = yield cocotb.external(dma.is_source_address_increment)(i)
        if r != True:
            raise cocotb.result.TestFailure("Channel [%d] DMA Source Address Increment not enabled" % (i))

        yield cocotb.external(dma.enable_source_address_increment)(i, False)
        r = yield cocotb.external(dma.is_source_address_increment)(i)
        if r:
            raise cocotb.result.TestFailure("Channel [%d] DMA Source Address Increment enabled" % (i))
        #Enable and Disable the source decrementing

        yield cocotb.external(dma.enable_source_address_decrement)(i, True)
        r = yield cocotb.external(dma.is_source_address_decrement)(i)
        if r != True:
            raise cocotb.result.TestFailure("Channel [%d] DMA Source Address Decrement not enabled" % (i))

        yield cocotb.external(dma.enable_source_address_decrement)(i, False)
        r = yield cocotb.external(dma.is_source_address_decrement)(i)
        if r:
            raise cocotb.result.TestFailure("Channel [%d] DMA Source Address Decrement enabled" % (i))

    for i in range (0, dma.sink_count):
        #Enable and Disable the dest incrementing
        yield cocotb.external(dma.enable_dest_address_increment)(i, True)
        r = yield cocotb.external(dma.is_dest_address_increment)(i)
        if r != True:
            raise cocotb.result.TestFailure("Channel [%d] DMA Sink Address Increment not enabled" % (i))

        yield cocotb.external(dma.enable_dest_address_increment)(i, False)
        r = yield cocotb.external(dma.is_dest_address_increment)(i)
        if r:
            raise cocotb.result.TestFailure("Channel [%d] DMA Sink Address Increment enabled" % (i))

        #Enable and Disable the dest decrementing
        yield cocotb.external(dma.enable_dest_address_decrement)(i, True)
        r = yield cocotb.external(dma.is_dest_address_decrement)(i)
        if r != True:
            raise cocotb.result.TestFailure("Channel [%d] DMA Sink Address Decrement not enabled" % (i))

        yield cocotb.external(dma.enable_dest_address_decrement)(i, False)
        r = yield cocotb.external(dma.is_dest_address_decrement)(i)
        if r:
            raise cocotb.result.TestFailure("Channel [%d] DMA Sink Address Decrement enabled" % (i))

        #Enable and Disable the sink respect quantum
        yield cocotb.external(dma.enable_dest_respect_quantum)(i, True)
        r = yield cocotb.external(dma.is_dest_respect_quantum)(i)
        if r != True:
            raise cocotb.result.TestFailure("Channel [%d] DMA Sink Address Respect Quantum not enabled" % (i))

        yield cocotb.external(dma.enable_dest_respect_quantum)(i, False)
        r = yield cocotb.external(dma.is_dest_respect_quantum)(i)
        if r:
            raise cocotb.result.TestFailure("Channel [%d] DMA Sink Address Respect Quantum enabled" % (i))



    r = nysa.response
    #print "response: %s" % str(r)
    yield nysa.wait_clocks(10)


def get_source_error_signal(dut, source_addr):
    source_ptr = None
    '''
    XXX

    This is ugly and should be fixed with a generator
    Maybe not, I'm not sure if I can parameterize all the input if I did a
    generator
    '''
    if source_addr == 0:
        source_ptr = dut.tdm0 
    elif source_addr == 1:
        source_ptr = dut.tdm1
    elif source_addr == 2:
        source_ptr = dut.tdm2
    elif source_addr == 3:
        source_ptr = dut.tdm3

    return source_ptr.m2f_data_error

def get_sink_error_signal(dut, sink_addr):
    sink_ptr = None
    '''
    XXX

    This is ugly and should be fixed with a generator
    Maybe not, I'm not sure if I can parameterize all the input if I did a
    generator
    '''
    if sink_addr == 0:
        sink_ptr = dut.tdm0 
    elif sink_addr == 1:
        sink_ptr = dut.tdm1
    elif sink_addr == 2:
        sink_ptr = dut.tdm2
    elif sink_addr == 3:
        sink_ptr = dut.tdm3

    return sink_ptr.f2m_data_error

   
class ErrorMonitor(cocotb.monitors.Monitor):

    def __init__(self, dut, signal):
        self.dut = dut
        self.signal = signal
        super (ErrorMonitor, self).__init__(callback = None, event = None)

    @cocotb.coroutine
    def _monitor_recv(self):
        while (1):
            yield cocotb.triggers.RisingEdge(self.signal)
            #self._recv(self.dut.get_sim_time())
            self._recv(1)

        

@cocotb.test(skip = False)
def test_execute_single_instruction(dut):
    """
    Description:
        -Setup source and sink for 256 word transaction
        -Setup the source address to increment
        -Setup the sink address to increment
        -setup instruction

    Test ID: 2

    Expected Results:
        Data is all transferred from one memory device to the next
    """
    dut.test_id = 2
    nysa = NysaSim(dut)
    yield(nysa.reset())
    nysa.read_sdb()
    yield nysa.wait_clocks(2000)

    dma = DMA(nysa, nysa.find_device(DMA)[0])
    yield cocotb.external(dma.setup)()
    yield cocotb.external(dma.enable_dma)(True)
    #yield nysa.wait_clocks(10)

    CHANNEL_ADDR = 0
    SINK_ADDR = 2
    INST_ADDR = 7

    source_error = get_source_error_signal(dut, CHANNEL_ADDR)
    sink_error = get_sink_error_signal(dut, SINK_ADDR)
    source_error_monitor = ErrorMonitor(dut, source_error)
    sink_error_monitor = ErrorMonitor(dut, sink_error)

    yield cocotb.external(dma.set_channel_sink_addr)            (CHANNEL_ADDR,  SINK_ADDR           )
    yield nysa.wait_clocks(10)
    yield cocotb.external(dma.set_channel_instruction_pointer)  (CHANNEL_ADDR,  INST_ADDR           )
    yield nysa.wait_clocks(10)
    yield cocotb.external(dma.enable_source_address_increment)  (CHANNEL_ADDR,  True                )
    yield nysa.wait_clocks(10)
    yield cocotb.external(dma.enable_dest_address_increment)    (SINK_ADDR,     True                )
    yield nysa.wait_clocks(10)
    yield cocotb.external(dma.enable_dest_respect_quantum)      (SINK_ADDR,     True                )
    yield nysa.wait_clocks(10)
    yield cocotb.external(dma.set_instruction_source_address)   (INST_ADDR,     0x0000000000000000  )
    yield nysa.wait_clocks(10)
    yield cocotb.external(dma.set_instruction_dest_address)     (INST_ADDR,     0x0000000000000010  )
    yield nysa.wait_clocks(10)
    yield cocotb.external(dma.set_instruction_count)            (INST_ADDR,     0x0100              )
    yield nysa.wait_clocks(10)
    yield cocotb.external(dma.set_channel_instruction_pointer)  (CHANNEL_ADDR,  INST_ADDR           )
    yield nysa.wait_clocks(10)
    #Start
    yield cocotb.external(dma.enable_channel)                   (CHANNEL_ADDR,  True                )

    yield nysa.wait_clocks(2000)
    yield cocotb.external(dma.enable_channel)                   (CHANNEL_ADDR,  False               )
    yield cocotb.external(dma.enable_dma)(False)
    yield nysa.wait_clocks(10)
    #dut.tdm0.m2f_data_error <= 1
    #yield nysa.wait_clocks(10)

    if len(source_error_monitor) > 0:
        print "Errors on source"

    if len(sink_error_monitor) > 0:
        print "Errors on sink"

    source_error_monitor.kill()
    sink_error_monitor.kill()




@cocotb.test(skip = False)
def test_continuous_transfer(dut):
    """
    Description:
        Setup a channel to transfer data

    Test ID: 3

    Expected Results:
        Data is all transferred from one memory device to the next
    """
    dut.test_id = 3
    nysa = NysaSim(dut)
    yield(nysa.reset())
    nysa.read_sdb()
    yield nysa.wait_clocks(2000)

    dma = DMA(nysa, nysa.find_device(DMA)[0])
    yield cocotb.external(dma.setup)()
    yield cocotb.external(dma.enable_dma)(True)
    #yield nysa.wait_clocks(10)

    CHANNEL_ADDR = 0
    SINK_ADDR = 2
    INST_ADDR = 7

    yield cocotb.external(dma.set_channel_sink_addr)            (CHANNEL_ADDR,  SINK_ADDR           )
    yield cocotb.external(dma.set_channel_instruction_pointer)  (CHANNEL_ADDR,  INST_ADDR           )
    yield cocotb.external(dma.enable_source_address_increment)  (CHANNEL_ADDR,  True                )
    yield cocotb.external(dma.enable_dest_address_increment)    (SINK_ADDR,     True                )
    yield cocotb.external(dma.enable_dest_respect_quantum)      (SINK_ADDR,     True                )
    yield cocotb.external(dma.enable_instruction_continue)      (INST_ADDR,     True                )
    yield cocotb.external(dma.set_instruction_source_address)   (INST_ADDR,     0x0000000000000000  )
    yield cocotb.external(dma.set_instruction_dest_address)     (INST_ADDR,     0x0000000000000010  )
    yield cocotb.external(dma.set_instruction_count)            (INST_ADDR,     0x0100              )
    yield cocotb.external(dma.set_instruction_next_instruction) (INST_ADDR,     INST_ADDR           )
    yield nysa.wait_clocks(10)

    #Start
    yield cocotb.external(dma.set_channel_instruction_pointer)  (CHANNEL_ADDR,  INST_ADDR           )
    yield cocotb.external(dma.enable_channel)                   (CHANNEL_ADDR,  True                )

    yield nysa.wait_clocks(2000)
    yield cocotb.external(dma.enable_channel)                   (CHANNEL_ADDR,  False               )
    yield cocotb.external(dma.enable_dma)(False)
    yield nysa.wait_clocks(10)



@cocotb.test(skip = False)
def test_double_buffer(dut):
    """
    Description:
        Setup a channel to transfer data

    Test ID: 4

    Expected Results:
        Data is all transferred from one memory device to the next
    """
    dut.test_id = 4
    nysa = NysaSim(dut)
    yield(nysa.reset())
    nysa.read_sdb()
    yield nysa.wait_clocks(2000)

    dma = DMA(nysa, nysa.find_device(DMA)[0])
    yield cocotb.external(dma.setup)()
    yield cocotb.external(dma.enable_dma)(True)
    #yield nysa.wait_clocks(10)

    CHANNEL_ADDR = 0
    SINK_ADDR = 2
    INST_ADDR = 7

    yield cocotb.external(dma.set_channel_sink_addr)            (CHANNEL_ADDR,  SINK_ADDR           )
    yield cocotb.external(dma.set_channel_instruction_pointer)  (CHANNEL_ADDR,  INST_ADDR           )
    yield cocotb.external(dma.enable_source_address_increment)  (CHANNEL_ADDR,  True                )
    yield cocotb.external(dma.enable_dest_address_increment)    (SINK_ADDR,     True                )
    yield cocotb.external(dma.enable_dest_respect_quantum)      (SINK_ADDR,     True                )
    yield cocotb.external(dma.enable_instruction_continue)      (INST_ADDR,     False               )
    yield cocotb.external(dma.set_instruction_source_address)   (INST_ADDR,     0x0000000000000000  )
    yield cocotb.external(dma.set_instruction_dest_address)     (INST_ADDR,     0x0000000000000010  )
    yield cocotb.external(dma.set_instruction_count)            (INST_ADDR,     0x0100              )
    yield cocotb.external(dma.set_instruction_next_instruction) (INST_ADDR,     INST_ADDR           )
    yield nysa.wait_clocks(10)

    #Start
    yield cocotb.external(dma.set_channel_instruction_pointer)  (CHANNEL_ADDR,  INST_ADDR           )
    yield cocotb.external(dma.enable_channel)                   (CHANNEL_ADDR,  True                )

    yield nysa.wait_clocks(2000)
    yield cocotb.external(dma.enable_channel)                   (CHANNEL_ADDR,  False               )
    yield cocotb.external(dma.enable_dma)(False)
    yield nysa.wait_clocks(10)


