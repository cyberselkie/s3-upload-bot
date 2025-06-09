import arc
import hikari

import src.func.s3 as s3

# For more info on plugins & extensions, see: https://arc.hypergonial.com/guides/plugins_extensions/

plugin = arc.GatewayPlugin("upload_files")

@plugin.include
@arc.slash_command("upload", "Upload an image or file to an S3 bucket")
async def upload(ctx: arc.GatewayContext, file: arc.Option[hikari.Attachment, arc.AttachmentParams(description="Image upload.", name=None)],
                 hidden: arc.Option[bool, arc.BoolParams("True or False")] = True) -> None:
        bucket = "selkie-images"
        image = s3.save_file(file.url, file.filename)
        s3.upload_file(image, bucket, file.title)
        url = s3.get_file_url(bucket, file.filename)
        s3.delete_file(file.filename)
        if hidden:
            await ctx.respond(f"File URL: <{url}>", flags=hikari.MessageFlag.EPHEMERAL)
        else: 
            await ctx.respond(f"File URL: {url}")


@plugin.include
@arc.message_command("Upload")
async def upload_file(ctx: arc.GatewayContext, message: hikari.Message) -> None:
        bucket = "selkie-images"
        response = "File URL:"
        for x in message.attachments:
            image = s3.save_file(x.url, x.filename)
            s3.upload_file(image, bucket, x.title)
            url = s3.get_file_url(bucket, x.filename)
            s3.delete_file(x.filename)
            response += f"\n{url}"

        await ctx.respond(response, flags=hikari.MessageFlag.EPHEMERAL)


@arc.loader
def load(client: arc.GatewayClient) -> None:
    client.add_plugin(plugin)


@arc.unloader
def unload(client: arc.GatewayClient) -> None:
    client.remove_plugin(plugin)
