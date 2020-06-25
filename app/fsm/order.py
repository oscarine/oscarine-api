from transitions import Machine


class OrderStatus(object):

    # Define different order status states.
    states = ['pending', 'accepted', 'declined', 'cancelled', 'delivered']

    def __init__(self, initial_state):

        # Initialize the state machine
        if initial_state in self.states:
            self.machine = Machine(
                model=self, states=OrderStatus.states, initial=initial_state
            )

        # Pending orders can be accepted and declined
        self.machine.add_transition(
            trigger='accept_order', source='pending', dest='accepted'
        )
        self.machine.add_transition(
            trigger='decline_order', source='pending', dest='declined'
        )

        # Accepted orders can change their status to delivered
        self.machine.add_transition(
            trigger='deliver_order', source='accepted', dest='delivered'
        )
