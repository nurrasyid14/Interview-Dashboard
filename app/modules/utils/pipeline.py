# utils/pipeline.py

class PipelineBlock:
    """Base class for pipeline blocks."""
    def run(self, *args, **kwargs):
        raise NotImplementedError("PipelineBlock must implement run().")

class CompositePipeline(PipelineBlock):
    """Runs multiple pipeline blocks in sequence."""
    def __init__(self, *blocks):
        self.blocks = blocks

    def run(self, data=None):
        """Sequentially passes output of each block to the next."""
        for block in self.blocks:
            data = block.run(data)
        return data
