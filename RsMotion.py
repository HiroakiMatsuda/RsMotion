#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-
# ver. 1.21117
# (C) 2012 Matsuda Hiroaki

"""
 \file RsMotion.py
 \brief It is the component that controls the RSX0X servo  from GUI.
 \date $Date$


"""
import sys
import time
sys.path.append(".")

# Import RTM module
import RTC
import OpenRTM_aist

# Inport Tkinter
import tkrsmotion

# Import Service implementation class
# <rtc-template block="service_impl">

# </rtc-template>

# Import Service stub modules
# <rtc-template block="consumer_import">
# </rtc-template>


# This module's spesification
# <rtc-template block="module_spec">
rsmotion_spec = ["implementation_id", "RsMotion", 
		 "type_name",         "RsMotion", 
		 "description",       "It is the component that controls the RSX0X servo from GUI.", 
		 "version",           "1.0.0", 
		 "vendor",            "Matsuda Hiroaki", 
		 "category",          "Motion", 
		 "activity_type",     "STATIC", 
		 "max_instance",      "1", 
		 "language",          "Python", 
		 "lang_type",         "SCRIPT",
		 ""]
# </rtc-template>

class RsMotion(OpenRTM_aist.DataFlowComponentBase):
	
	"""
	\class RsMotion
	\brief It is the component that controls the RSX0X servo  from GUI.
	
	"""
	
	def __init__(self, manager):
		"""
		\brief constructor
		\param manager Maneger Object
		"""
		OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

		self._d_sens = RTC.TimedLongSeq(RTC.Time(0,0),[])
		"""
		"""
		self._sensIn = OpenRTM_aist.InPort("sens", self._d_sens)

		self._d_motion = RTC.TimedLongSeq(RTC.Time(0,0),[])
		"""
		"""
		self._motionOut = OpenRTM_aist.OutPort("motion", self._d_motion)
		self._d_on_off = RTC.TimedLongSeq(RTC.Time(0,0),[])
		"""
		"""
		self._on_offOut = OpenRTM_aist.OutPort("on_off", self._d_on_off)


		# initialize of configuration-data.
		# <rtc-template block="init_conf_param">
		
		# </rtc-template>


		 
	def onInitialize(self):
		"""
		
		The initialize action (on CREATED->ALIVE transition)
		formaer rtc_init_entry() 
		
		\return RTC::ReturnCode_t
		
		"""
		# Bind variables and configuration variable
		
		# Set InPort buffers
		self.addInPort("sens",self._sensIn)
		
		# Set OutPort buffers
		self.addOutPort("motion",self._motionOut)
		self.addOutPort("on_off",self._on_offOut)
		
		# Set service provider to Ports
		
		# Set service consumers to Ports
		
		# Set CORBA Service Ports

		self.motion_data = []
		self.past_data = []
		
		return RTC.RTC_OK
	
	
	def onActivated(self, ec_id):
		"""
	
		The activated action (Active state entry action)
		former rtc_active_entry()
	
		\param ec_id target ExecutionContext Id
	
		\return RTC::ReturnCode_t
	
		"""
	
		return RTC.RTC_OK
	
	def onDeactivated(self, ec_id):
		"""
	
		The deactivated action (Active state exit action)
		former rtc_active_exit()
	
		\param ec_id target ExecutionContext Id
	
		\return RTC::ReturnCode_t
	
		"""
	
		return RTC.RTC_OK
	
	def onExecute(self, ec_id):
		"""
	
		The execution action that is invoked periodically
		former rtc_active_do()
	
		\param ec_id target ExecutionContext Id
	
		\return RTC::ReturnCode_t
	
		"""
		if self.past_data != self.motion_data:
                        print('Motion: %s' % self.motion_data)
                        self._d_motion.data = self.motion_data
                        OpenRTM_aist.setTimestamp(self._d_motion)
                        self._motionOut.write()
                        self.past_data = self.motion_data
		
		if self._sensIn.isNew():
                        self.read_data()
                        
		return RTC.RTC_OK

        #def set_value(self, pos, pol):
        #        self.on = pos[0]
        #        self.motion = pos[1]

        def send_data(self, data):
                if len(data) == 4:
                        self.motion_data = data  
                        
                elif len(data) == 3:
                        print('Servo ON/OFF: %s' % data)
                        self._d_on_off.data = data
                        OpenRTM_aist.setTimestamp(self._d_on_off)
                        self._on_offOut.write()

        def read_data(self):
                self._d_sens = self._sensIn.read()
                return self._d_sens.data

#def RsMotionInit(manager):
#    profile = OpenRTM_aist.Properties(defaults_str=rsmotion_spec)
#    manager.registerFactory(profile,
#                            RsMotion,
#                            OpenRTM_aist.Delete)
#
#def MyModuleInit(manager):
#    RsMotionInit(manager)
#
#    # Create a component
#    comp = manager.createComponent("RsMotion")

def main():
        tk = tkrsmotion.TkRsMotion()
	mgr = OpenRTM_aist.Manager.init(sys.argv)
	mgr.activateManager()
	# Register component
	profile = OpenRTM_aist.Properties(defaults_str=rsmotion_spec)
	mgr.registerFactory(profile,
                            RsMotion,
                            OpenRTM_aist.Delete)
	comp = mgr.createComponent("RsMotion")
	tk.get_out_port(comp.send_data)
	tk.get_in_port(comp.read_data)
	mgr.runManager(True)
	tk.root.mainloop()

if __name__ == "__main__":
	main()

