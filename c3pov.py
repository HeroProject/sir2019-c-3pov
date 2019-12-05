from conversation import conversation
from io_mapper.Nao import Nao
from nao.C3POVApplication import C3POVApplication

lang = 'en-US'
dfKey = 'newagent-xsfpqi-7709b1d68262.json'
dfAgent = 'newagent-xsfpqi'

c3pov = C3POVApplication(lang, dfKey, dfAgent)
io = Nao(c3pov)

conversation(io)

# Stopping the thread at the end of execution
c3pov.stop()
