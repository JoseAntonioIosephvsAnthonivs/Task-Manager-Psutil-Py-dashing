from dashing import HSplit, VSplit, VGauge, HGauge, Text
from psutil import (
	virtual_memory,
 	swap_memory,
 	cpu_percent,
 	sensors_battery,
 	net_if_addrs,
 	net_if_stats,
 	net_io_counters,
 	pids,
 	process_iter
 )
from time import sleep

def bytes_to_gigas(value):
	return  value /1024 / 1024 / 1024 

def bytes_to_megas(value):
	return value / 1024 / 1024

ui = HSplit(  
	VSplit(
		Text(
			' ',
			border_color=9,
			title= 'Procedures',
			color= 9

		),
		HSplit( 
			VGauge(title='RAM'),#ui.items[0],itens[0]
			VGauge(title='SWAP'),#ui.items[0],itens[0]
			title='Memory',
			border_color=9
		),
	),
	VSplit( 
		HGauge(title='CPU %'),
		HGauge(title='cpu_1 %'),
		HGauge(title='cpu_2 %'),
		HGauge(title='cpu_3 %'),
		HGauge(title='cpu_4 %'),
		HGauge(title='cpu_5 %'),
		HGauge(title='cpu_6 %'),
		HGauge(title='cpu_7 %'),
		HGauge(title='CPU Temp'),
		title='CPU',
		border_color=9
	
	),
	VSplit(  
		Text(
			' ',
			title= 'Others',
			border_color=9,
			color=9
		),
		Text(
			' ',
			title='WEB',
			border_color=9,
			color=9
		)
	)
)


while True:
#Procedures##############################################
	proc_tui = ui.items[0].items[0]
	p_list = []
	for proc in process_iter():
		proc_info = proc.as_dict(['name', 'cpu_percent'])
		if proc_info['cpu_percent'] > 0:
			p_list.append(proc_info)

	ordenados = sorted(
		p_list,
		key=lambda p: p['cpu_percent'],
		reverse=True
	)[:10]
	proc_tui.text = f"{'Name':<30}CPU"

	for proc in ordenados:
		proc_tui.text += f"\n {proc['name']:<30} {proc['cpu_percent']}"
	proc_tui.text += f'\n Processos: {len(pids())}'

#Memoria##################################################
	mem_tui = ui.items[0].items[1]
#RAM#####################################################
	ram_tui = mem_tui.items[0]
	ram_tui.value = virtual_memory().percent
	ram_tui.title = f'RAM {ram_tui.value} %'
#SWAP###################################################
	swap_tui = mem_tui.items[1]
	swap_tui.value = swap_memory().percent
	swap_tui.title = f'SWAP {swap_tui.value} %'
#CPU####################################################
	cpu_tui = ui.items[1]
#CPU %###################################################
	cpu_percent_tui = cpu_tui.items[0]
	ps_cpu_percent = cpu_percent()
	cpu_percent_tui. value = ps_cpu_percent
	cpu_percent_tui.title = f'CPU {ps_cpu_percent} %'                                               
#Porcentagem dos cores####################################
	cpu_percent_tui.value = ps_cpu_percent
	cpu_percent_tui.title = f'CPU {ps_cpu_percent} %'
	cores_tui = cpu_tui.items[1:9]
	ps_cpu_percent = cpu_percent(percpu=True)
	for i, (core, value) in enumerate(zip(cores_tui, ps_cpu_percent)):
		core.value = value
		core.title = f'cpu_{i} {value}%'
#Outros###################################################
	outros_tui = ui.items[2].items[0]
	outros_tui.text = f'Battery {sensors_battery().percent} %'
#Rede####################################################
	network_tui = ui.items[2].items[1]
	addrs_v4 = net_if_addrs()['Wi-Fi'][0]
	addrs_v6 = net_if_addrs()['Wi-Fi'][1]
	network_tui.text = f'IPV4: {addrs_v4.address}\n'
	network_tui.text += f'MaskV4: {addrs_v4.netmask}\n'
	network_tui.text += f'IPV6: {addrs_v6.address[:10]} \n'
	network_tui.text += f'MaskV6: {addrs_v6.netmask} \n'

	network_tui.text += f'Sent: {bytes_to_gigas(net_io_counters().bytes_sent):.2f}GB\n'
	network_tui.text += f'Recceived: {bytes_to_gigas(net_io_counters().bytes_recv):.2f}GB\n'



	try:
		ui.display()
		sleep(1)
	except KeyboardInterrupt:
		break
