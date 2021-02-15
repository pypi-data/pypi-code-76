import numpy as np

class BatchHeatmapUtils:
    @classmethod
    def flatten_batch_heatmaps(self, batch_heatmaps: np.ndarray, batch_size: int, num_joints: int) -> np.ndarray:
        return batch_heatmaps.reshape((batch_size, num_joints, -1))

    @classmethod
    def find_flattened_heatmap_maxvals(self, flattened_heatmaps: np.ndarray, batch_size: int, num_joints: int):
        # find index of max value in each heatmap
        flat_idx = np.argmax(flattened_heatmaps, axis=2)

        # find max value in each heatmap
        flat_maxvals = np.amax(flattened_heatmaps, axis=2)

        # Reshape to isolate maxvals and maxvals indicies
        flat_idx = flat_idx.reshape((batch_size, num_joints, 1)) 
        flat_maxvals = flat_maxvals.reshape((batch_size, num_joints, 1))

        return flat_idx, flat_maxvals

    @classmethod
    def get_unflattened_coords(self, flattened_idx: np.ndarray, heatmap_width: int) -> np.ndarray:
        # Start to build prediction coords using x = y = flattened index.
        coords = np.tile(flattened_idx, (1, 1, 2)).astype(np.float32)

        # Convert flattened indecies to actual (x, y) coordinates
        coords[:, :, 0] = (coords[:, :, 0]) % heatmap_width # x = x % heatmap_width for each x coordinate
        coords[:, :, 1] = np.floor((coords[:, :, 1]) / heatmap_width) # y = y / heatmap_width for each y coordinate
        
        # Now we have the actual (x, y) coordinates of the location of the maxval in each heatmap
        return coords

    @classmethod
    def zero_negative_maxval_coords(self, coords: np.ndarray, maxvals: np.ndarray) -> np.ndarray:
        # get pred_mask where positive values -> 1 and negative values -> 0
        coords_mask = np.tile(np.greater(maxvals, 0.0), (1, 1, 2)).astype(np.float32)
        # Change coordinates that coorespond to negative maxvals to (0, 0)
        return coords * coords_mask

def get_maxvals_and_coords(batch_heatmaps: np.ndarray) -> (np.ndarray, np.ndarray):
    batch_size, num_joints, height, width = batch_heatmaps.shape

    # Flatten heatmaps for maximum search
    flattened_heatmaps = BatchHeatmapUtils.flatten_batch_heatmaps(
        batch_heatmaps=batch_heatmaps,
        batch_size=batch_size,
        num_joints=num_joints
    )

    # Find maxval and maxval index in flattened heatmaps
    idx, maxvals = BatchHeatmapUtils.find_flattened_heatmap_maxvals(
        flattened_heatmaps=flattened_heatmaps,
        batch_size=batch_size,
        num_joints=num_joints
    )

    # Convert maxval index to (x, y) coordinates
    coords = BatchHeatmapUtils.get_unflattened_coords(
        flattened_idx=idx,
        heatmap_width=width
    )

    # Filter out negative maxval coordinates
    coords = BatchHeatmapUtils.zero_negative_maxval_coords(coords=coords, maxvals=maxvals)
    return coords, maxvals