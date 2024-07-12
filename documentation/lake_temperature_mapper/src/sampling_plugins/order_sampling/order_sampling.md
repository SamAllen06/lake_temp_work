# Order Sampling (APP/src/sampling_plugins/order_sampling/)

## Purpose
Order Sampling is a sampling plugin that uses "order files" to generate
[Order(s)](order.md), a subclass of [SampleGroup.](../../sampling/sample_group.md)

## Functionality
Order Sampling uses "order files" (json files with instructions for linearly
interpolating through the input space.) Order files can either include data
for a [LineOrder](line_order.md) or [BoxOrder](box_order.md).

Each order file will become its own [SampleGroup.](../../sampling/sample_group.md)
