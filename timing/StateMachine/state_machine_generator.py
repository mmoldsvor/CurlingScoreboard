from graphviz import Digraph

def generate_graph(active_node):
    d = Digraph('G', filename=f'state_machine_{active_node}.gv', format='svg')

    with d.subgraph() as s:
        s.attr(rank='same')
        if active_node == 'no_touch_no_motion':
            s.node('no_touch_no_motion', label='Default\nState', shape='doublecircle', fillcolor='#7eeda5', style='filled')
        else:
            s.node('no_touch_no_motion', label='Default\nState', shape='doublecircle')

    with d.subgraph() as s:
        s.attr(rank='same')
        if active_node == 'touch':
            s.node('touch', label='T:1 M:0', shape='circle', fillcolor='#7eeda5', style='filled')
        else:
            s.node('touch', label='T:1 M:0', shape='circle')

        if active_node == 'motion_no_touch':
            s.node('motion_no_touch', label='T:0 M:1', shape='circle', fillcolor='#7eeda5', style='filled')
        else:
            s.node('motion_no_touch', label='T:0 M:1', shape='circle')

        if active_node == 'no_motion':
            s.node('no_motion', label='T:0 M:0', shape='circle', fillcolor='#7eeda5', style='filled')
        else:
            s.node('no_motion', label='T:0 M:0', shape='circle')
            

    with d.subgraph() as s:
        s.attr(rank='same')
        if active_node == 'touch_motion':
            s.node('touch_motion', label='T:1 M:1', shape='circle', fillcolor='#7eeda5', style='filled')
        else:
            s.node('touch_motion', label='T:1 M:1', shape='circle')

        if active_node == 'motion':
            s.node('motion', label='T:0 M:1', shape='circle', fillcolor='#7eeda5', style='filled')
        else:
            s.node('motion', label='T:0 M:1', shape='circle')
    

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
    for node in nodes:
        generate_graph(node)

    