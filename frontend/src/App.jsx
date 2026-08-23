import { useEffect, useRef, useState } from 'react'
import './App.css'

const SEED_LOGS = [
  { type: 'INFO', text: '192.168.1.50 -> 10.0.0.1 | TCP 80 | HTTP GET /api/v1/health 200' },
  { type: 'WARN', text: '192.168.1.105 | RULE MATCH: Brute force login threshold exceeded' },
  { type: 'ALERT', text: 'PFSENSE_BLOCK | Dropped inbound connection from 45.33.32.156' },
  { type: 'INFO', text: '172.16.0.5 -> 10.0.0.1 | UDP 53 | DNS QUERY OK' },
]

const INITIAL_THREATS = [
  { id: 1, sourceIp: '192.168.1.105', eventType: 'Brute Force (5x Fail)', score: 85, severity: 'CRITICAL' },
  { id: 2, sourceIp: '10.0.0.42', eventType: 'Port Scan Pattern', score: 65, severity: 'HIGH' },
  { id: 3, sourceIp: '172.16.0.12', eventType: 'Blacklisted IP Access', score: 50, severity: 'MEDIUM' },
]

const INITIAL_SEVERITY = [
  { label: 'CRITICAL (81-100)', pct: 15, color: 'var(--crit-purple)' },
  { label: 'HIGH (61-80)', pct: 30, color: 'var(--alert-red)' },
  { label: 'MEDIUM (31-60)', pct: 40, color: 'var(--warn-yellow)' },
  { label: 'LOW (0-30)', pct: 15, color: 'var(--text-green)' },
]

function pad(n) {
  return n.toString().padStart(2, '0')
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
}

const logClassByType = {
  WARN: 'warn',
  ALERT: 'alert',
}

function App() {
  const [clock, setClock] = useState(nowStr())
  const [bootTime] = useState(() => new Date().toDateString())
  const [totalLogs, setTotalLogs] = useState(14285)
  const [threats, setThreats] = useState(INITIAL_THREATS)
  const [logs, setLogs] = useState([
    { type: 'INFO', time: '[14:02:15]', text: '192.168.1.1 -> 10.0.0.1 | TCP 443 | ACK_OK' },
    { type: 'WARN', time: '[14:02:14]', text: '192.168.1.105 | AUTH_FAIL (attempt 5/5)' },
    { type: 'ALERT', time: '[14:02:11]', text: 'PFSENSE Firewall | DENY 185.220.101.5:80' },
  ])
  const logContainerRef = useRef(null)

  useEffect(() => {
    const clockTimer = setInterval(() => setClock(nowStr()), 1000)

    const streamTimer = setInterval(() => {
      const log = SEED_LOGS[Math.floor(Math.random() * SEED_LOGS.length)]
      setLogs((prev) => [...prev.slice(-100), { ...log, time: `[${nowStr()}]` }])
      setTotalLogs((prev) => prev + 1)
    }, 2000)

    return () => {
      clearInterval(clockTimer)
      clearInterval(streamTimer)
    }
  }, [])

  useEffect(() => {
    if (logContainerRef.current) {
      logContainerRef.current.scrollTop = logContainerRef.current.scrollHeight
    }
  }, [logs])

  const activeThreats = threats.filter((t) => !t.resolved).length
  const criticalIncidents = threats.filter((t) => t.severity === 'CRITICAL' && !t.resolved).length

  function resolveThreat(id) {
    setThreats((prev) =>
      prev.map((t) => (t.id === id ? { ...t, resolved: true } : t)),
    )
  }

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
            <div className="status">
              [WS_LOGS: CONNECTED <span className="cursor" />]
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
                    <tr key={t.id} style={t.resolved ? { opacity: 0.3 } : undefined}>
                      <td>{t.sourceIp}</td>
                      <td>{t.eventType}</td>
                      <td>{t.score}/100</td>
                      <td>
                        <span className={`tag ${severityClass[t.severity]}`}>{t.severity}</span>
                      </td>
                      <td>
                        <button
                          type="button"
                          className="btn-term"
                          disabled={t.resolved}
                          onClick={() => resolveThreat(t.id)}
                        >
                          {t.resolved ? '[RESOLVED]' : '[RESOLVE]'}
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
                {INITIAL_SEVERITY.map((s) => (
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
                <div key={i} className={`log-line ${logClassByType[log.type] ?? 'info'}`}>
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
