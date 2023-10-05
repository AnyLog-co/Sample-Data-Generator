class Snetio:
    """
    Convert snetio from string to JSON format
    """
    def __init__(self, bytes_sent, bytes_recv, packets_sent, packets_recv, errin, errout, dropin, dropout):
        self.bytes_sent = int(bytes_sent)
        self.bytes_recv = int(bytes_recv)
        self.packets_sent = int(packets_sent)
        self.packets_recv = int(packets_recv)
        self.errin = int(errin)
        self.errout = int(errout)
        self.dropin = int(dropin)
        self.dropout = int(dropout)