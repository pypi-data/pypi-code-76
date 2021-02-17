from circle import resources

OBJECT_CLASSES = {
    resources.Ach.OBJECT_NAME: resources.Ach,
    resources.Card.OBJECT_NAME: resources.Card,
    resources.Message.OBJECT_NAME: resources.Message,
    resources.Notification.OBJECT_NAME: resources.Notification,
    resources.Payment.OBJECT_NAME: resources.Payment,
    resources.Payout.OBJECT_NAME: resources.Payout,
    resources.Wire.OBJECT_NAME: resources.Wire,
    resources.WireInstruction.OBJECT_NAME: resources.WireInstruction,
}
