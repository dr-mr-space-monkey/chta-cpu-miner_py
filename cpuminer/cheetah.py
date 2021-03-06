import time
from datetime import datetime
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

def run_cheetah(prevheight, rpc_user,rpc_password,rpc_port, cpu):
   

   # rpc_user and rpc_password are set in the bitcoin.conf file
   rpc_connection = AuthServiceProxy("http://%s:%s@127.0.0.1:%d"%(rpc_user, rpc_password, rpc_port))
   
   bestblock_index = rpc_connection.getblockcount()
   bestblock_hash = rpc_connection.getblockhash(bestblock_index)   
   bestblock = rpc_connection.getblock(bestblock_hash)   

   cur_epoch = int(time.time()) 
   
   bcstucktime = cur_epoch - bestblock['time']

   if bcstucktime < 0:
      print "Height {} block Time is ahead of current time {} seconds, possible miner cheating on timestamp, current {} GMT".format(bestblock['height'], bcstucktime, datetime.utcnow())
      
   mining_info = rpc_connection.getmininginfo()
   
   if ( bcstucktime > 120 ):
      print "ASIC/GPU miners got stuck on CHTA blockchain for {} seconds".format(bcstucktime)
      print "Cheetah running, block {}: {} {} GMT".format(bestblock['height'],bestblock['time'], datetime.utcnow())
      
      if not mining_info['generate']:
         print("Cheetah accelerates, CHTA CPU Mining Started")
         rpc_connection.setgenerate(True, cpu)
      elif bestblock['height'] != prevheight:
         print("Cheetah jumps, CHTA CPU Mining Restarted")
         rpc_connection.setgenerate(False)
         rpc_connection.setgenerate(True, cpu)
   else:
      if mining_info['generate']:
         print "block {}: {} {} GMT".format(bestblock['height'],bestblock['time'], datetime.utcnow())
         print("Cheetah rests, CHTA CPU Mining Stopped")
         rpc_connection.setgenerate(False)


   return bestblock['height']

   
   

         

