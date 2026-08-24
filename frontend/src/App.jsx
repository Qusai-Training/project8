import { useEffect, useRef, useState } from 'react'
import './App.css'

function pad(n) {
  return (n ?? 0).toString().padStart(2, '0')
}

function nowStr() {
  const d = new Date()
  return `${pad(d.getHours())}:${pad(d.getMinutes())}:${pad(d.getSeconds())}`
}

const severityClass = {
  CRITICAL: 'tag-crit',
  HIGH: 'tag-high',
  MEDIUM: 'tag-med',
  LOW: 'tag-low',
  Critical: 'tag-crit',
  High: 'tag-high',
  Medium: 'tag-med',
  Low: 'tag-low',
}

function App() {
  const [clock, setClock] = useState(nowStr())
  const [bootTime] = useState(() => new Date().toDateString())
  const [totalLogs, setTotalLogs] = useState(0)
  const [threats, setThreats] = useState([])
  const [logs, setLogs] = useState([])
  const [severityStats, setSeverityStats] = useState({ low: 0, medium: 0, high: 0, critical: 0, total_threats: 0 })
  const [wsConnected, setWsConnected] = useState(false)
  
  const logContainerRef = useRef(null)
  const wsRef = useRef(null)

  // 1. Live Clock
  useEffect(() => {
    const clockTimer = setInterval(() => setClock(nowStr()), 1000)
    return () => clearInterval(clockTimer)
  }, [])

  // 2. Fetch Initial API Data (REST Endpoints)
  useEffect(() => {
    // Fetch Recent Logs
    fetch('http://localhost:8000/api/logs/recent?limit=50')
      .then((res) => res.json())
      .then((data) => {
        if (Array.isArray(data)) {
          const formatted = data.map((item) => ({
            type: item.severity ? item.severity.toUpperCase() : 'INFO',
            time: `[${new Date(item.created_at || Date.now()).toLocaleTimeString()}]`,
            text: `${item.source_ip} -> ${item.destination_ip || '127.0.0.1'} | ${item.event_type} | ${item.raw_message}`
          }))
          setLogs(formatted)
          setTotalLogs(data.length)
        }
      })
      .catch((err) => console.error('Error fetching logs:', err))

    // Fetch Initial Threat Alerts
    fetch('http://localhost:8000/api/threats')
      .then((res) => res.json())
      .then((data) => {
        if (Array.isArray(data)) {
          setThreats(data)
        }
      })
      .catch((err) => console.error('Error fetching threats:', err))

    // Fetch Threat Statistics
    fetch('http://localhost:8000/api/threats/stats')
      .then((res) => res.json())
      .then((data) => {
        if (data && data.total_threats !== undefined) {
          setSeverityStats(data)
        }
      })
      .catch((err) => console.error('Error fetching threat stats:', err))
  }, [])

  // 3. Connect Real-time WebSocket Stream (/ws/logs)
  useEffect(() => {
    const ws = new WebSocket('ws://localhost:8000/ws/logs')
    wsRef.current = ws

    ws.onopen = () => {
      setWsConnected(true)
    }

    ws.onclose = () => {
      setWsConnected(false)
    }

    ws.onmessage = (event) => {
      try {
        const message = JSON.parse(event.data)
        
        // Handle incoming new logs
        if (message.event === 'new_log') {
          const data = message.data
          const newEntry = {
            type: data.severity ? data.severity.toUpperCase() : 'INFO',
            time: `[${nowStr()}]`,
            text: `${data.source_ip} -> ${data.destination_ip || '127.0.0.1'} | ${data.event_type} | ${data.raw_message}`
          }
          setLogs((prev) => [...prev.slice(-100), newEntry])
          setTotalLogs((prev) => prev + 1)
        }

        // Handle incoming threat alerts
        if (message.event === 'threat_alert') {
          const threatData = message.data
          setThreats((prev) => [threatData, ...prev])
          setSeverityStats((prev) => ({
            ...prev,
            total_threats: prev.total_threats + 1,
            [threatData.threat_type.toLowerCase()]: (prev[threatData.threat_type.toLowerCase()] || 0) + 1
          }))
        }
      } catch (err) {
        console.error('Error parsing WS message:', err)
      }
    }

    return () => {
      ws.close()
    }
  }, [])

  // Auto-scroll log console to bottom on update
  useEffect(() => {
    if (logContainerRef.current) {
      logContainerRef.current.scrollTop = logContainerRef.current.scrollHeight
    }
  }, [logs])

  const activeThreats = threats.filter((t) => !t.is_resolved).length
  const criticalIncidents = threats.filter(
    (t) => (t.threat_type?.toUpperCase() === 'CRITICAL') && !t.is_resolved
  ).length

  function resolveThreat(id) {
    setThreats((prev) =>
      prev.map((t) => (t.id === id ? { ...t, is_resolved: true } : t))
    )
  }

  // Calculate dynamic severity breakdown percentages
  const total = severityStats.total_threats || 1
  const severityDistribution = [
    { label: 'CRITICAL (81-100)', pct: Math.round(((severityStats.critical || 0) / total) * 100), color: 'var(--crit-purple)' },
    { label: 'HIGH (61-80)', pct: Math.round(((severityStats.high || 0) / total) * 100), color: 'var(--alert-red)' },
    { label: 'MEDIUM (31-60)', pct: Math.round(((severityStats.medium || 0) / total) * 100), color: 'var(--warn-yellow)' },
    { label: 'LOW (0-30)', pct: Math.round(((severityStats.low || 0) / total) * 100), color: 'var(--text-green)' },
  ]

  return (
    <div className="app-root crt-flicker">
      <div className="crt-overlay" />
      <div className="crt-vignette" />

      <div className="terminal-window">
        <div className="title-bar">
          <div className="dot dot-red" />
          <div className="dot dot-yellow" />
          <div className="dot dot-green" />
          <div className="title-bar-text">root@monitoring-sys — /var/log/secops — 80x24</div>
          <div className="title-bar-clock">{clock}</div>
        </div>

        <div className="term-body">
          <div className="boot-line">Last login: {bootTime} from 10.0.0.7 on ttys004</div>
          <div className="prompt-line">
            <span className="prompt-sym">root@sec01</span>
            :~$ ./realtime_monitor --daemon --stream=/ws/logs
          </div>

          <div className="header">
            <div className="title">&gt; REAL_TIME_MONITORING_SYSTEM // VER 2.4.0</div>
            <div className="status" style={{ color: wsConnected ? 'var(--text-green)' : 'var(--alert-red)' }}>
              [{wsConnected ? 'WS_LOGS: CONNECTED' : 'WS_LOGS: DISCONNECTED'} <span className="cursor" />]
            </div>
          </div>

          <div className="kpi-row">
            <div className="kpi-box">
              <div className="kpi-label">SYS_PARSED_LOGS</div>
              <div className="kpi-val">{totalLogs.toLocaleString()}</div>
            </div>
            <div className="kpi-box">
              <div className="kpi-label">ACTIVE_THREATS</div>
              <div className="kpi-val" style={{ color: 'var(--alert-red)' }}>
                {pad(activeThreats)}
              </div>
            </div>
            <div className="kpi-box">
              <div className="kpi-label">CRITICAL_INCIDENTS</div>
              <div className="kpi-val" style={{ color: 'var(--crit-purple)' }}>
                {pad(criticalIncidents)}
              </div>
            </div>
            <div className="kpi-box">
              <div className="kpi-label">BLACKLISTED_IPS</div>
              <div className="kpi-val">048</div>
            </div>
          </div>

          <div className="main-grid">
            <div className="panel">
              <div className="panel-header">
                <span>&gt; ACTIVE_THREAT_MONITOR</span>
                <span className="ph-tag">[LIVE]</span>
              </div>
              <table>
                <thead>
                  <tr>
                    <th>SOURCE_IP</th>
                    <th>EVENT_TYPE</th>
                    <th>SCORE</th>
                    <th>SEVERITY</th>
                    <th>ACTION</th>
                  </tr>
                </thead>
                <tbody>
                  {threats.map((t) => (
                    <tr key={t.id} style={t.is_resolved ? { opacity: 0.3 } : undefined}>
                      <td>{t.source_ip || t.sourceIp || '127.0.0.1'}</td>
                      <td>{t.description || t.eventType}</td>
                      <td>{t.threat_score ?? t.score}/100</td>
                      <td>
                        <span className={`tag ${severityClass[t.threat_type || t.severity]}`}>
                          {(t.threat_type || t.severity)?.toUpperCase()}
                        </span>
                      </td>
                      <td>
                        <button
                          type="button"
                          className="btn-term"
                          disabled={t.is_resolved}
                          onClick={() => resolveThreat(t.id)}
                        >
                          {t.is_resolved ? '[RESOLVED]' : '[RESOLVE]'}
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            <div className="panel">
              <div className="panel-header">
                <span>&gt; SEVERITY_METRICS</span>
              </div>
              <div className="dist-section">
                {severityDistribution.map((s) => (
                  <div key={s.label}>
                    <span>
                      {s.label} - {s.pct}%
                    </span>
                    <div className="dist-bar">
                      <span className="dist-fill" style={{ width: `${s.pct}%`, background: s.color }} />
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          <div className="panel">
            <div className="panel-header">
              <span>&gt; STREAM_INGEST_FEED (/ws/logs)</span>
              <span className="ph-tag">tail -f</span>
            </div>
            <div className="terminal-stream" ref={logContainerRef}>
              {logs.map((log, i) => (
                <div key={i} className={`log-line ${log.type === 'WARN' ? 'warn' : log.type === 'ALERT' || log.type === 'HIGH' || log.type === 'CRITICAL' ? 'alert' : 'info'}`}>
                  {log.time} {log.type.padEnd(5)} | {log.text}
                </div>
              ))}
            </div>
          </div>

          <div className="footer-prompt">
            <span className="prompt-sym">root@sec01</span>:~$ <span className="cursor" />
          </div>
        </div>
      </div>
    </div>
  )
}

export default App