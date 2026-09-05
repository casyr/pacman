# pacman

Here is the function-by-function mapping from MiniLibX (mlx) to Pygame.

Because MiniLibX relies on an event-driven hook system in C while Pygame uses an object-oriented Python structure with an explicit main loop, the approaches differ slightly in practice.

| MiniLibX Function | Pygame Equivalent | Notes / Differences |
| --- | --- | --- |
| **Initialization** |  |  |
| `mlx_init` | `pygame.init()` | Initializes all imported Pygame modules. |
| `mlx_new_window` | `pygame.display.set_mode((w, h))` | Creates the display window and returns the main screen `Surface`. |
| `mlx_clear_window` | `screen.fill((R, G, B))` | Fills a Surface (e.g., screen) with a specific color. |
| `mlx_destroy_window` | `pygame.display.quit()` | Uninitializes the display module and closes the window. |
| **Util functions** |  |  |
| `mlx_get_color_value` | `pygame.Color(r, g, b, a)` | Pygame handles colors directly via `(R, G, B)` tuples or the `Color` class. |
| `mlx_pixel_put` | `surface.set_at((x, y), color)` | Draws a single pixel. (Rarely used directly in Pygame due to performance; array manipulation is preferred). |
| `mlx_string_put` | `font.render()` then `screen.blit()` | Requires creating a `pygame.font.Font` object, generating a text Surface with `.render()`, then drawing it. |
| **Image functions** |  |  |
| `mlx_new_image` | `pygame.Surface((w, h))` | Creates a new blank image/surface in memory. |
| `mlx_get_data_addr` | `pygame.surfarray.pixels3d()` or `surface.get_buffer()` | Accesses pixel data directly as arrays or raw memory buffers. |
| `mlx_put_image_to_window` | `screen.blit(image_surface, (x, y))` | Draws one Surface onto another (e.g., onto the screen). Requires calling `pygame.display.flip()` to render. |
| `mlx_destroy_image` | `del image_surface` | Memory is freed automatically by Python's Garbage Collector when references are removed. |
| **Hooks / Loop** |  |  |
| `mlx_mouse_hook` | `pygame.event.get()` loop | Handled via `pygame.MOUSEBUTTONDOWN` and `pygame.MOUSEBUTTONUP` event types. |
| `mlx_key_hook` | `pygame.event.get()` loop | Handled via `pygame.KEYDOWN` and `pygame.KEYUP` event types. |
| `mlx_expose_hook` | `pygame.VIDEOEXPOSE` or loop redrawing | Handled explicitly inside your main `while` loop. |
| `mlx_loop_hook` | `while running:` loop body | Code inside the explicit main loop runs every frame. |
| `mlx_loop` | `while running:` + `pygame.time.Clock().tick(FPS)` | Pygame does not hide the loop behind a callback framework; you write the explicit `while` loop. |
| **Image conversions** |  |  |
| `mlx_xpm_to_image` | N/A (No direct native equivalent) | Requires parsing XPM string data manually or converting via Pillow (`PIL`). |
| `mlx_xpm_file_to_image` | `pygame.image.load("file.xpm")` | Loads an image file from disk (supports XPM if compiled with SDL_image support). |
| `mlx_png_file_to_image` | `pygame.image.load("file.png")` | Natively loads PNG images from disk. |
| **Mouse functions** |  |  |
| `mlx_mouse_hide` | `pygame.mouse.set_visible(False)` | Hides the mouse cursor. |
| `mlx_mouse_show` | `pygame.mouse.set_visible(True)` | Shows the mouse cursor. |
| `mlx_mouse_move` | `pygame.mouse.set_pos((x, y))` | Sets the mouse cursor position to the specified coordinates. |
| `mlx_mouse_get_pos` | `pygame.mouse.get_pos()` | Returns an `(x, y)` tuple of the mouse's current position. |
| **Key auto repeat** |  |  |
| `mlx_do_key_autorepeatoff` | `pygame.key.set_repeat()` | Disables key repetition (default Pygame behavior). |
| `mlx_do_key_repeaton` | `pygame.key.set_repeat(delay, interval)` | Enables repeating `KEYDOWN` events when holding a key. |
| **Un-categorized** |  |  |
| `mlx_do_sync` | `pygame.display.flip()` or `pygame.display.update()` | Updates the full display surface to the screen. |
| `mlx_get_screen_size` | `pygame.display.Info().current_w`, `.current_h` | Fetches the current display monitor resolution. |