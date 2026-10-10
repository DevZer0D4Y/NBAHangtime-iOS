import GameController

@main
struct GamepadTests {
    static func main() {
        let controllers = (0..<4).map { _ in GCController.withExtendedGamepad() }
        var connected = controllers
        let hub = GamepadHub(controllerProvider: { connected })
        _ = hub.poll(now: 0)
        for (slot, controller) in controllers.enumerated() {
            let g = controller.extendedGamepad!
            g.buttonX.setValue(1); g.buttonA.setValue(1); g.rightTrigger.setValue(1)
            g.leftThumbstick.xAxis.setValue(-1); g.buttonMenu.setValue(1)
            let down = hub.poll(now: 1)
            assert(down.players[slot].held == [.shoot, .pass, .turbo])
            assert(down.players[slot].directions == Pad.left)
            assert(controller.playerIndex.rawValue == GamepadHub.playerOrder[slot])
            g.buttonMenu.setValue(0)
            let tap = hub.poll(now: 1.1)
            assert(tap.players[slot].startTap)
            assert(tap.players.enumerated().allSatisfy { $0.offset == slot || !$0.element.startTap })
            g.buttonX.setValue(0); g.buttonA.setValue(0); g.rightTrigger.setValue(0)
            g.leftThumbstick.xAxis.setValue(0)
            _ = hub.poll(now: 1.2)
        }
        connected.reverse()
        controllers[1].extendedGamepad!.buttonA.setValue(1)
        assert(hub.poll(now: 2).players[1].held == [.pass])
        hub.suppressHeldButtons()
        assert(hub.poll(now: 2.1).players[1].held.isEmpty)
        controllers[1].extendedGamepad!.buttonA.setValue(0)
        _ = hub.poll(now: 2.2)
        controllers[1].extendedGamepad!.buttonA.setValue(1)
        assert(hub.poll(now: 2.3).players[1].held == [.pass])
        connected.removeAll { $0 === controllers[0] }
        let disconnected = hub.poll(now: 3)
        assert(disconnected.players.count == 4 && disconnected.players[0].held.isEmpty)
        assert(disconnected.players[1].held == [.pass])
        let replacement = GCController.withExtendedGamepad()
        connected.append(replacement)
        replacement.extendedGamepad!.buttonMenu.setValue(1)
        _ = hub.poll(now: 4)
        assert(hub.poll(now: 4.7).events.contains(.pause))
        replacement.extendedGamepad!.buttonMenu.setValue(0)
        assert(!hub.poll(now: 4.8).players[0].startTap)
        assert(replacement.playerIndex.rawValue == 0)
        var sequence = ActionSequencer()
        sequence.pulseStart()
        for _ in 0..<6 { assert(sequence.frame(directions: 0, held: [], sprint: false) == Pad.start) }
        assert(sequence.frame(directions: 0, held: [], sprint: false) == 0)
        print("Gamepads: four-player inputs, start order, stable slots, reconnect, suppression and pause passed.")
    }
}
