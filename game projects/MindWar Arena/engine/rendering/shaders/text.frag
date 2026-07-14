#version 330 core

in vec2 uv;

out vec4 fragColor;

uniform sampler2D text_texture;

void main()
{
    fragColor = texture(
        text_texture,
        uv
    );
}