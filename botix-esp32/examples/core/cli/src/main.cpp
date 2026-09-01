#include <kf/main.hpp>
#include <kf/rtos/Clock.hpp>
#include <kf/rtos/Task.hpp>

#include "botix/cli/Config.hpp"
#include "botix/cli/Console.hpp"
#include "botix/transport/Kind.hpp"

void kf::main(kf::Init &init) {
    init.logger.debug("hello test");

    botix::cli::Config cli_console_config{};

    botix::cli::Channel channels[1]{
        botix::cli::Channel{init.arena, cli_console_config, {.echo = true}},
    };

    botix::cli::Console console{init.arena, cli_console_config, channels};

    auto &channel = console.channels()[0];

    auto maybe_group = console.addGroup(init.arena, {.name = "transport"});

    botix::cli::Argument kek_arguments[]{
        {
            {.name{"a"}},
            botix::cli::Argument::Integer{
                .params{.default_value{123}},
                .min_value{-100},
                .max_value{200},
            },
        },
        {{.name{"boo"}},
         botix::cli::Argument::Boolean{
             .params{.default_value{false}},
         }},
    };

    auto maybe_command = maybe_group.unwrap().addCommand(
        init.arena,
        {
            .name = "kek",
            .description = "do important stuff",
            .shortcut = kf::some('e'),
        },
        kek_arguments,
        [&init](botix::cli::Command::Context const &context) {
            auto const e = context.arguments[0].integer();
            context.channel.output.print("cmd:'{}': {}", context.channel.input_line, e);
        });

    if (maybe_command.isNone()) {
        init.logger.error("command fail");
        return;
    }

    botix::cli::Argument::Enum::Item const transports[]{
        {{.name = "espnow", .description{"use ESPNOW transport"}}, botix::transport::Kind::Espnow},
        {{.name = "wifi", .description{"this option has no shortcut"}, .shortcut = kf::none}, botix::transport::Kind::Wifi},
    };

    init.logger.debug("arena available: {}", init.arena.available());

    while (true) {
        auto const now = rtos::Clock::now();

        if (channel.output.availableForRead() > 0) {
            init.logger.debug("output: {}", channel.output.drain());
        }

        while (init.io.availableForRead() > 0) {
            if (auto read = init.io.readByte(); read.isOk()) {
                (void) channel.input.feed({reinterpret_cast<char const *>(&read.ok()), 1});
            }
        }

        console.poll(now);
        rtos::Task::sleep(1);
    }
}