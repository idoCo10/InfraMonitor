from inframonitor_agent.collectors.disk import collect_disk_info


def test_disk_info():
    disk_info = collect_disk_info()

    assert disk_info is not None
    assert "disks" in disk_info
    assert "total_disks" in disk_info

    assert isinstance(disk_info["disks"], list)
    assert disk_info["total_disks"] == len(disk_info["disks"])

    for disk in disk_info["disks"]:
        assert disk["name"]
        assert disk["size"]
        assert disk["type"] == "disk"

        assert "bus" in disk
        assert "media_type" in disk
        assert "vendor" in disk
        assert "model" in disk
        assert "serial" in disk
        assert "partitions" in disk

        assert isinstance(disk["partitions"], list)

        for partition in disk["partitions"]:
            assert partition["name"]
            assert partition["size"]
            assert partition["type"]

            assert "filesystem" in partition
            assert "mountpoints" in partition
            assert "usage" in partition
            assert "logical_volumes" in partition

            # Partition filesystem usage
            if partition["usage"] is not None:
                usage = partition["usage"]

                assert usage["total_bytes"] > 0
                assert usage["used_bytes"] >= 0
                assert usage["free_bytes"] >= 0
                assert 0 <= usage["utilization_percent"] <= 100

            # LVM logical volumes
            for lv in partition["logical_volumes"]:
                assert lv["name"]
                assert lv["size"]
                assert lv["type"] == "lvm"

                assert "filesystem" in lv
                assert "mountpoints" in lv
                assert "usage" in lv

                if lv["usage"] is not None:
                    usage = lv["usage"]

                    assert usage["total_bytes"] > 0
                    assert usage["used_bytes"] >= 0
                    assert usage["free_bytes"] >= 0
                    assert 0 <= usage["utilization_percent"] <= 100