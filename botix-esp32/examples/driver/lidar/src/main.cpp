#include <kf/Array.hpp>
#include <kf/main.hpp>

#include "botix/driver/sensor/Lidar.hpp"

void kf::main(kf::Init &init) {

    init.logger.info("lidar example");

    static botix::driver::sensor::Lidar::Config config{
        .uart{
            .baudrate = 115'200,
            .rx_buffer_length{0x04'00},
        },
        .min_distance_mm{20},
        .max_distance_mm{2000},
        .min_intensity{15},
    };

    static botix::driver::sensor::Lidar lidar_driver{{
        .common_config = config,
        .specific_config{
            .uart_num = 2,
            .rx_gpio_num = kf::gpio::G16,
            .tx_gpio_num = kf::gpio::G17,
        },
    }};

    init.logger.info("lidar running: {}", lidar_driver.running());

    init.logger.info("lidar init");
    lidar_driver.init();

    init.logger.info("lidar running: {}", lidar_driver.running());

    constexpr int sector_count = 8;
    constexpr int sector_size = 360 / sector_count;// 45
    constexpr auto invalid = botix::driver::sensor::Lidar::Data::invalid_value;

    for (int i = 0; i < 10000; i += 1) {
        auto const &data = lidar_driver.read().distances_mm;

        u32 sums[sector_count]{};
        u8 counts[sector_count]{};

        for (int i = 0; i < 360; i += 1) {
            auto val = data[i];
            if (val == invalid) { continue; }

            int sector = i / sector_size;
            sums[sector] += val;
            counts[sector] += 1;
        }

        Array<u16, sector_count> avg{};
        for (int s = 0; s < sector_count; s += 1) {
            if (counts[s] > 0) {
                avg[s] = static_cast<u16>(sums[s] / counts[s]);
            } else {
                avg[s] = invalid;
            }
        }

        init.logger.info("sectors: {}", avg);
        delay(100);
    }

    init.logger.info("lidar quit");
    lidar_driver.quit();
    init.logger.info("lidar running: {}", lidar_driver.running());

    delay(1000);
    init.logger.info("lidar running: {}", lidar_driver.running());
}