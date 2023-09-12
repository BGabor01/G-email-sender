class RpcResponse:
    def __init__(self, success: bool, message: str = None):
        """
        Initialize an RpcResponse object.

        Parameters
        ----------
        success : bool
            A boolean indicating whether the RPC call was successful.
        message : str, optional
            A message providing details about the success or failure of the RPC call.
        """
        self.success = success
        self.message = message

    def __repr__(self):
        return f"<RpcResponse(success={self.success}, message={self.message})>"

    @property
    def is_successful(self) -> bool:
        """Check if the RPC call was successful."""
        return self.success

    @property
    def get_message(self) -> str:
        """Get the message related to the RPC call."""
        return self.message
