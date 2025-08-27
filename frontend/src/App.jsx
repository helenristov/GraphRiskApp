import React, { useEffect, useState } from 'react'
import CytoscapeComponent from 'react-cytoscapejs'
import axios from 'axios'

export default function App(){
  const [graph, setGraph] = useState({nodes:[], edges:[]})

  useEffect(()=>{ fetchGraph() }, [])

  async function fetchGraph(){
    const {data} = await axios.get('http://localhost:8000/graph')
    setGraph(data)
  }

  const elements = [
    ...graph.nodes.map(n => ({ data: { id: n.id, label: n.label, type: n.type }})),
    ...graph.edges.map((e,i) => ({ data: { id: `e${i}`, source: e.source, target: e.target, label: e.type }}))
  ]

  const style = [
    { selector: 'node', style: { 'label': 'data(label)' } },
    { selector: 'node[type="ThirdParty"]', style: { 'shape':'ellipse', 'background-color':'#5ba' } },
    { selector: 'node[type="Risk"]', style: { 'shape':'diamond', 'background-color':'#e85' } },
    { selector: 'edge', style: { 'curve-style':'bezier', 'label':'data(label)' } }
  ]

  return (
    <div style={{width:'100%', height:'100vh'}}>
      <CytoscapeComponent elements={elements} style={{ width: '100%', height: '100%' }} stylesheet={style} layout={{ name: 'cose' }} />
    </div>
  )
}
