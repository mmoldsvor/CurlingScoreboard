from graphviz import Digraph

def generate_graph(active_node):
    d = Digraph('G', filename=f'state_machine_{active_node}.gv', format='svg')
    d.graph_attr.update(size="15,15")

    with d.subgraph() as s:
        s.attr(rank='same')
        if active_node == 'no_touch_no_motion':
            s.node('no_touch_no_motion', label='Default\nState', shape='doublecircle', fillcolor='#7eeda5', style='filled', fontname = "calibri")
        else:
            s.node('no_touch_no_motion', label='Default\nState\n\nAlle steiner i\n systemet står\n i ro', shape='doublecircle', fontname = "calibri", width="2.5", fixedsize="true")

    with d.subgraph() as s:
        s.attr(rank='same')
        if active_node == 'touch':
            s.node('touch', label='T:1 M:0', shape='circle', fillcolor='#7eeda5', style='filled', fontname = "calibri")
        else:
            s.node('touch', label='T:1 M:0\n\nTouch men ikke\n bevegelse', shape='circle', fontname = "calibri", width="2.5", fixedsize="true")

        if active_node == 'motion_no_touch':
            s.node('motion_no_touch', label='T:0 M:1', shape='circle', fillcolor='#7eeda5', style='filled', fontname = "calibri")
        else:
            s.node('motion_no_touch', label='T:0 M:1\n\nBevegelse men\n ikke touch', shape='circle', fontname = "calibri", width="2.5", fixedsize="true")

        if active_node == 'no_motion':
            s.node('no_motion', label='T:0 M:0', shape='circle', fillcolor='#7eeda5', style='filled', fontname = "calibri")
        else:
            s.node('no_motion', label='T:0 M:0\n\nEn annen stein\n enn den som\n ble kastet er\n i bevegelse', shape='circle', fontname = "calibri", width="2.5", fixedsize="true")
            

    with d.subgraph() as s:
        s.attr(rank='same')
        if active_node == 'touch_motion':
            s.node('touch_motion', label='T:1 M:1', shape='circle', fillcolor='#7eeda5', style='filled', fontname = "calibri")
        else:
            s.node('touch_motion', label='T:1 M:1\n\nTouch og\n bevegelse', shape='circle', fontname = "calibri", width="2.5", fixedsize="true")

        if active_node == 'motion':
            s.node('motion', label='T:0 M:1', shape='circle', fillcolor='#7eeda5', style='filled', fontname = "calibri")
        else:
            s.node('motion', label='T:0 M:1\n\nStein har blitt\n sluppet og er nå\n satt i spill', shape='circle', fontname = "calibri", width="2.5", fixedsize="true")
    

    d.edge('no_touch_no_motion', 'touch')
    d.edge('touch', 'no_touch_no_motion')
    d.edge('no_touch_no_motion', 'motion_no_touch')
    d.edge('motion_no_touch', 'no_touch_no_motion')
    d.edge('motion_no_touch', 'touch_motion')
    d.edge('touch', 'touch_motion')
    d.edge('touch_motion', 'motion')
    d.edge('motion', 'no_motion')
    d.edge('no_motion', 'no_touch_no_motion')
    
    d.view()

if __name__ == '__main__':
    nodes = ['no_touch_no_motion', 'touch', 'motion_no_touch', 'touch_motion', 'motion', 'no_motion', 'none']
    
    generate_graph('detailed')
    # for node in nodes:
        # generate_graph(node)
