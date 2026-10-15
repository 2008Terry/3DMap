import QtQuick

Canvas {
    id: root
    required property var state
    objectName: "structurePlan"
    readonly property var plan: state.plan
    readonly property real padding: 12
    readonly property real scaleFactor: plan.bounds ? Math.min((width - padding * 2) / (plan.bounds[2] - plan.bounds[0]),
                                                               (height - padding * 2) / (plan.bounds[3] - plan.bounds[1])) : 1
    readonly property real originX: plan.bounds ? (width - (plan.bounds[2] - plan.bounds[0]) * scaleFactor) / 2 : 0
    readonly property real originY: plan.bounds ? (height - (plan.bounds[3] - plan.bounds[1]) * scaleFactor) / 2 : 0
    function px(x) { return originX + (x - plan.bounds[0]) * scaleFactor }
    function py(z) { return originY + (z - plan.bounds[1]) * scaleFactor }
    function drawRegions(ctx, regions, fill, stroke) {
        for (let region of regions || []) {
            ctx.beginPath()
            for (let ring of [region.outer].concat(region.holes)) {
                for (let i = 0; i < ring.length; ++i) {
                    const x = px(ring[i][0]), y = py(ring[i][1])
                    if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y)
                }
                ctx.closePath()
            }
            ctx.fillStyle = fill; ctx.fill()
            if (stroke) { ctx.strokeStyle = stroke; ctx.lineWidth = 1; ctx.stroke() }
        }
    }
    onPlanChanged: requestPaint()
    onWidthChanged: requestPaint()
    onHeightChanged: requestPaint()
    onPaint: {
        const ctx = getContext("2d")
        ctx.clearRect(0, 0, width, height)
        if (!plan.bounds) return
        drawRegions(ctx, plan.footprint, "#eff1e8", "#647d7c")
        drawRegions(ctx, plan.corridor, "#a9d6d5", "")
        for (let room of plan.rooms) {
            const selected = state.selected_space.id === room.id
            drawRegions(ctx, room.regions, selected ? "#efbd65" : "#d4ddd5", "#647d7c")
            ctx.fillStyle = selected ? "#422d14" : "#35514e"
            ctx.font = "10px sans-serif"
            ctx.fillText(String(room.index + 1), px(room.x) - 3, py(room.z) + 3)
        }
        drawRegions(ctx, plan.walls, "#294b50", "")
        if (plan.route.length > 1) {
            ctx.beginPath()
            for (let i = 0; i < plan.route.length; ++i) {
                const p = plan.route[i]
                if (i === 0) ctx.moveTo(px(p[0]), py(p[1])); else ctx.lineTo(px(p[0]), py(p[1]))
            }
            ctx.strokeStyle = "#e7832e"; ctx.lineWidth = 3; ctx.stroke()
        }
        if (plan.core.x !== undefined) {
            ctx.beginPath(); ctx.arc(px(plan.core.x), py(plan.core.z), 5, 0, Math.PI * 2)
            ctx.fillStyle = "#168d9d"; ctx.fill()
        }
    }
    MouseArea {
        anchors.fill: parent
        onClicked: function(mouse) {
            if (!root.plan.bounds) return
            root.state.pick_plan((mouse.x - root.originX) / root.scaleFactor + root.plan.bounds[0],
                                 (mouse.y - root.originY) / root.scaleFactor + root.plan.bounds[1])
        }
    }
}
